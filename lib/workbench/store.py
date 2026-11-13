"""Transactional local storage. Backups are validated before a single row changes."""

from contextlib import contextmanager
from dataclasses import dataclass
import hashlib
import logging
import os
from pathlib import Path
import sqlite3
import tempfile
from typing import Callable

from pydantic import ValidationError

from .models import Backup, Recipe, Run, RunState, SavedRecipe, StepCheckpoint, new_id, now
from .backups import archive_backup, read_backup, JSON_LIMIT

logger = logging.getLogger(__name__)


class Conflict(ValueError):
    """A stale page or another active run makes this action unsafe to repeat."""


@dataclass(frozen=True)
class RunSummary:
    id: str
    topic: str
    title: str
    state: str
    mode: str
    updated_at: str
    saved_steps: int
    total_steps: int
    resume_note: str
    archived: bool


_SUMMARY_SQL = """
    SELECT id, json_extract(payload, '$.topic'), json_extract(payload, '$.recipe.title'),
           state, coalesce(json_extract(payload, '$.mode'), 'live'), updated,
           json_array_length(payload, '$.results'), json_array_length(payload, '$.recipe.steps'),
           coalesce(json_extract(payload, '$.resume_note'), '')
    FROM runs
"""


class Store:
    def __init__(self, directory: str | Path):
        self.directory = Path(directory).expanduser().resolve()
        self.directory.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.path = self.directory / "studio.sqlite3"
        self.pending_path = self.directory / "pending-step.json"
        try:
            os.close(os.open(self.path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600))
        except FileExistsError:
            pass
        with self.connection() as db:
            db.execute("PRAGMA journal_mode=WAL")
            db.execute("CREATE TABLE IF NOT EXISTS recipes (id TEXT PRIMARY KEY, payload TEXT NOT NULL)")
            db.execute("CREATE TABLE IF NOT EXISTS runs (id TEXT PRIMARY KEY, state TEXT NOT NULL, updated TEXT NOT NULL, payload TEXT NOT NULL)")
            db.execute("CREATE INDEX IF NOT EXISTS runs_updated ON runs(updated DESC)")
            db.execute("CREATE INDEX IF NOT EXISTS runs_state ON runs(state)")
            db.execute("CREATE TABLE IF NOT EXISTS import_receipts (kind TEXT NOT NULL, fingerprint TEXT NOT NULL, PRIMARY KEY (kind, fingerprint))")

    @contextmanager
    def connection(self):
        db = sqlite3.connect(self.path, timeout=10)
        try:
            db.execute("PRAGMA synchronous=FULL")
            with db:
                yield db
        finally:
            db.close()

    def save_recipe(self, recipe: Recipe, topic: str = "", context: str = "", review_each: bool = True) -> SavedRecipe:
        saved = SavedRecipe(recipe=recipe, topic=topic, context=context, review_each=review_each)
        with self.connection() as db:
            db.execute("INSERT INTO recipes VALUES (?, ?)", (saved.id, saved.model_dump_json()))
        return saved

    def get_recipe(self, recipe_id: str) -> SavedRecipe:
        with self.connection() as db:
            row = db.execute("SELECT payload FROM recipes WHERE id = ?", (recipe_id,)).fetchone()
        if row is None:
            raise KeyError("That recipe was not found.")
        return SavedRecipe.model_validate_json(row[0])

    def recipes(self) -> list[SavedRecipe]:
        with self.connection() as db:
            rows = db.execute("SELECT payload FROM recipes ORDER BY rowid DESC").fetchall()
        return [SavedRecipe.model_validate_json(row[0]) for row in rows]

    def create_run(self, run: Run) -> Run:
        # Validate even when a caller has built a model using model_copy/update.
        run = Run.model_validate(run.model_dump())
        with self.connection() as db:
            self._insert_run(db, run)
        return run

    def open_example(self, create: Callable[[], Run]) -> Run:
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            for (payload,) in db.execute(
                "SELECT payload FROM runs WHERE json_valid(payload) AND json_extract(payload, '$.mode') = 'example'"
            ):
                try:
                    return Run.model_validate_json(payload)
                except ValidationError:
                    continue  # An unreadable earlier example remains on disk for recovery.
            run = create()
            self._insert_run(db, run)
            return run

    @staticmethod
    def _insert_run(db, run: Run):
        db.execute("INSERT INTO runs VALUES (?, ?, ?, ?)",
                   (run.id, run.state, run.updated_at, run.model_dump_json()))

    def get_run(self, run_id: str) -> Run:
        with self.connection() as db:
            return self._get_run(db, run_id)

    @staticmethod
    def _get_run(db, run_id: str) -> Run:
        row = db.execute("SELECT payload FROM runs WHERE id = ?", (run_id,)).fetchone()
        if row is None:
            raise KeyError("That run was not found. Your other saved work is still in the library.")
        return Run.model_validate_json(row[0])

    def runs(self, query: str = "", limit: int | None = 100) -> list[Run]:
        with self.connection() as db:
            rows = db.execute("SELECT payload FROM runs ORDER BY updated DESC").fetchall()
        runs = [Run.model_validate_json(row[0]) for row in rows]
        if query.strip():
            term = query.casefold().strip()
            runs = [r for r in runs if term in f"{r.topic} {r.recipe.title} {r.state}".casefold()]
        return runs if limit is None else runs[:limit]

    def run_summaries(self, query: str = "", *, limit: int = 100, offset: int = 0,
                      archived: bool = False) -> list[RunSummary]:
        where = "WHERE json_valid(payload) AND coalesce(json_extract(payload, '$.archived'), 0) = ?"
        arguments = [archived]
        term = query.casefold().strip()
        with self.connection() as db:
            if term:
                db.create_function("casefold", 1, lambda value: str(value or "").casefold())
                where += """
                    AND instr(casefold(json_extract(payload, '$.topic') || ' ' ||
                                       json_extract(payload, '$.recipe.title') || ' ' || state), ?) > 0
                """
                arguments.append(term)
            rows = db.execute(
                _SUMMARY_SQL + where + " ORDER BY updated DESC, id LIMIT ? OFFSET ?",
                (*arguments, limit, offset),
            ).fetchall()
        return [RunSummary(*row, archived=archived) for row in rows]

    def resume_run(self) -> RunSummary | None:
        with self.connection() as db:
            row = db.execute(_SUMMARY_SQL + """
                WHERE json_valid(payload) AND state != 'completed'
                      AND coalesce(json_extract(payload, '$.archived'), 0) = 0
                ORDER BY (state = 'running') DESC, updated DESC, id LIMIT 1
            """).fetchone()
        return RunSummary(*row, archived=False) if row else None

    def running_ids(self) -> list[str]:
        with self.connection() as db:
            return [row[0] for row in db.execute("SELECT id FROM runs WHERE state = 'running'")]

    def set_resume_note(self, run_id: str, note: str, revision: int) -> Run:
        note = note.strip()
        if len(note) > 1000:
            raise ValueError("The resume note can contain up to 1,000 characters.")
        return self.mutate(run_id, lambda run: setattr(run, "resume_note", note), revision)

    def set_archived(self, run_id: str, archived: bool, revision: int) -> Run:
        def change(run):
            if run.state == "running":
                raise Conflict("Pause this run before archiving it.")
            run.archived = archived
        return self.mutate(run_id, change, revision)

    def fork_run(self, run_id: str, step_count: int, revision: int) -> Run:
        """Copy a live checkpoint or start a Chain Lab remix from its plan."""
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            parent = self._get_run(db, run_id)
            if parent.revision != revision:
                raise Conflict("This run changed. Reload it before creating a branch.")
            if parent.mode == "lab" and step_count == 0:
                if parent.archived or parent.state not in {"paused", "completed"}:
                    raise Conflict("Choose an active or finished Chain Lab plan to remix.")
                remix = Run(
                    recipe=parent.recipe, topic=parent.topic, context=parent.context, model=parent.model,
                    mode="lab", parent_run_id=parent.id, forked_after_step=0,
                )
                self._insert_run(db, remix)
                return remix
            if parent.mode != "live" or parent.state == "running":
                raise Conflict("Choose a stopped live run to branch from.")
            if not 1 <= step_count <= min(len(parent.results), len(parent.recipe.steps) - 1):
                raise ValueError("Choose a saved step before the end of the chain.")
            branch = Run(
                recipe=parent.recipe, topic=parent.topic, context=parent.context, model=parent.model,
                state="paused", review_each=parent.review_each, results=parent.results[:step_count],
                parent_run_id=parent.id, forked_after_step=step_count,
            )
            self._insert_run(db, branch)
        return branch

    def mutate(self, run_id: str, change: Callable[[Run], None], revision: int | None = None) -> Run:
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            run = self._get_run(db, run_id)
            if revision is not None and run.revision != revision:
                raise Conflict("This run changed in another tab. Reload it before continuing.")
            change(run)
            run.updated_at = now()
            run.revision += 1
            run = Run.model_validate(run.model_dump())
            db.execute("UPDATE runs SET state = ?, updated = ?, payload = ? WHERE id = ?",
                       (run.state, run.updated_at, run.model_dump_json(), run.id))
        return run

    def claim(self, run_id: str, revision: int) -> Run:
        # The running check and transition share a write transaction: two tabs
        # cannot dispatch the same step or start overlapping provider work.
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            if db.execute("SELECT 1 FROM runs WHERE state = 'running' LIMIT 1").fetchone():
                raise Conflict("A chain is already running. Open it in your library, or wait for its current step to finish.")
            run = self._get_run(db, run_id)
            if run.revision != revision:
                raise Conflict("This run changed. Reload it before continuing.")
            if run.mode != "live":
                raise Conflict("Only live runs can send a model request.")
            if run.archived:
                raise Conflict("Move this run out of the archive before continuing.")
            if run.state == "completed":
                raise Conflict("This run is already complete. Start a fresh run to use it again.")
            run.state, run.error, run.pause_requested = "running", "", False
            run.execution_id, run.review_notice = new_id(), ""
            run.updated_at = now()
            run.revision += 1
            db.execute("UPDATE runs SET state = ?, updated = ?, payload = ? WHERE id = ?",
                       (run.state, run.updated_at, run.model_dump_json(), run.id))
        return run

    @staticmethod
    def stop(run: Run, state: RunState):
        run.state = state
        run.pause_requested = False
        run.execution_id = None
        run.active_attempt_id = None

    def begin_step(self, run_id: str, execution_id: str, *, stop_before_dispatch: bool = False) -> Run:
        """Serialize the right to dispatch this step against pause."""
        def begin(current):
            if current.state != "running" or current.execution_id != execution_id or current.active_attempt_id:
                raise Conflict("This execution no longer owns the next step.")
            if current.pause_requested or stop_before_dispatch:
                self.stop(current, "paused")
            else:
                current.active_attempt_id = new_id()
        return self.mutate(run_id, begin)

    def finish_step(self, checkpoint: StepCheckpoint, *, stop_after_save: bool = False) -> Run:
        def finish(current):
            if (current.execution_id != checkpoint.execution_id
                    or (checkpoint.attempt_id is not None and current.active_attempt_id != checkpoint.attempt_id)):
                if checkpoint.result and any(result.attempt_id == checkpoint.attempt_id for result in current.results):
                    if stop_after_save and current.state == "running" and current.execution_id == checkpoint.execution_id:
                        self.stop(current, "paused")
                    return  # The earlier save reached SQLite before its caller received confirmation.
                raise Conflict("This step no longer belongs to the active execution.")
            if checkpoint.result is None:
                self.stop(current, "failed")
                current.error = checkpoint.error
                return
            current.results.append(checkpoint.result)
            current.active_attempt_id = None
            reason = checkpoint.result.finish_reason
            if reason and reason != "stop":
                current.review_notice = (
                    "The answer reached the configured token limit. Review the saved text before using it."
                    if reason == "length"
                    else "The model reported an unusual completion. Review the saved text before using it."
                )
            if len(current.results) == len(current.recipe.steps):
                self.stop(current, "completed")
            elif current.review_each or current.pause_requested or current.review_notice or stop_after_save:
                self.stop(current, "paused")
        return self.mutate(checkpoint.run_id, finish)

    def read_pending_checkpoint(self) -> StepCheckpoint | None:
        try:
            with self.pending_path.open("rb") as stream:
                raw = stream.read(JSON_LIMIT + 1)
        except FileNotFoundError:
            return None
        if len(raw) > JSON_LIMIT:
            raise ValueError("The pending checkpoint exceeds its size limit.")
        return StepCheckpoint.model_validate_json(raw)

    def write_pending_checkpoint(self, checkpoint: StepCheckpoint):
        descriptor, name = tempfile.mkstemp(prefix=".pending-step-", dir=self.directory)
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
                stream.write(checkpoint.model_dump_json())
                stream.flush()
                os.fsync(stream.fileno())
            # Refuse to overwrite a prior journal if it could not be preserved.
            os.link(name, self.pending_path)
        finally:
            Path(name).unlink(missing_ok=True)

    def preserve_pending_checkpoint(self):
        self.pending_path.rename(self.directory / f"unmatched-step-{new_id()}.json")

    def recover(self, *, preserve_run_id: str | None = None) -> int:
        """Called only while holding the application's exclusive runtime lock."""
        recovered = 0
        for run_id in self.running_ids():
            if run_id == preserve_run_id:
                continue

            def interrupt(current):
                self.stop(current, "interrupted")
                current.error = ("The app stopped during this step. Completed steps are safe. "
                                 "The provider may have processed the unfinished request; check its usage before retrying.")

            try:
                self.mutate(run_id, interrupt)
            except ValidationError:
                # Release the old execution's claim while preserving the original
                # payload for recovery from a stopped workspace-folder copy.
                with self.connection() as db:
                    db.execute("UPDATE runs SET state = 'interrupted' WHERE id = ? AND state = 'running'", (run_id,))
                logger.warning("Preserved an unreadable Studio run. Its previous execution no longer owns the workspace.")
            recovered += 1
        return recovered

    def backup(self) -> Backup:
        recipes, runs = self._snapshot()
        if len(recipes) > 2000 or len(runs) > 2000:
            raise ValueError("Use a Studio ZIP archive for more than 2,000 recipes or runs.")
        backup = Backup(recipes=recipes, runs=runs)
        if len(backup.model_dump_json(indent=2).encode("utf-8")) > JSON_LIMIT:
            raise ValueError("This JSON backup exceeds its restore limit. Use a .zip backup instead.")
        return backup

    def archive(self) -> bytes:
        return archive_backup(*self._snapshot())

    def _snapshot(self) -> tuple[list[SavedRecipe], list[Run]]:
        # One read transaction provides a consistent snapshot even during a run.
        with self.connection() as db:
            db.execute("BEGIN")
            try:
                recipes = [SavedRecipe.model_validate_json(row[0]) for row in db.execute("SELECT payload FROM recipes")]
                runs = [Run.model_validate_json(row[0]) for row in db.execute("SELECT payload FROM runs")]
            except ValidationError:
                raise ValueError("Saved work contains an unreadable record. Preserve a stopped workspace-folder copy.") from None
        from .runner import validate_recipe
        try:
            for record in [*recipes, *runs]:
                validate_recipe(record.recipe)
        except ValueError:
            raise ValueError("Saved work contains an invalid recipe reference. Preserve a stopped workspace-folder copy before repairing it.") from None
        return recipes, runs

    def restore(self, raw: bytes) -> tuple[int, int]:
        recipes, runs = read_backup(raw)
        from .runner import validate_recipe
        for records in (recipes, runs):
            for record in records:
                validate_recipe(record.recipe)
                if isinstance(record, Run):
                    if record.state == "running":
                        self.stop(record, "interrupted")
                        record.error = "Restored during an unfinished step. Check provider usage before retrying it."
                    record.pause_requested = False
                type(record).model_validate_json(record.model_dump_json())
        # Import adds records. Matching records are skipped; different records
        # with the same ID receive a fresh ID, so local work is never overwritten.
        counts = [0, 0]
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            for kind, records in enumerate((recipes, runs)):
                table = "recipes" if kind == 0 else "runs"
                for record in records:
                    existing = db.execute(f"SELECT payload FROM {table} WHERE id = ?", (record.id,)).fetchone()
                    if existing and self._matches(existing[0], record):
                        continue
                    if existing:
                        fingerprint = hashlib.sha256(
                            ("studio-import-v1:" + record.model_dump_json()).encode()
                        ).hexdigest()
                        if db.execute(
                            "SELECT 1 FROM import_receipts WHERE kind = ? AND fingerprint = ?",
                            (table, fingerprint),
                        ).fetchone():
                            continue
                        db.execute("INSERT INTO import_receipts VALUES (?, ?)", (table, fingerprint))
                        record.id = fingerprint[:32]
                        imported = db.execute(f"SELECT payload FROM {table} WHERE id = ?", (record.id,)).fetchone()
                        if imported and self._matches(imported[0], record):
                            continue
                        if imported:
                            record.id = new_id()
                    if kind == 1:
                        self._insert_run(db, record)
                    else:
                        db.execute("INSERT INTO recipes VALUES (?, ?)", (record.id, record.model_dump_json()))
                    counts[kind] += 1
        return tuple(counts)

    @staticmethod
    def _matches(payload: str, record: SavedRecipe | Run) -> bool:
        try:
            return type(record).model_validate_json(payload) == record
        except ValueError:
            return False
