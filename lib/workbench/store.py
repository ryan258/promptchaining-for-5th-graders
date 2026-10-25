"""Transactional local storage. Backups are validated before a single row changes."""

from contextlib import contextmanager
from pathlib import Path
import sqlite3
from typing import Callable
import hashlib

from .models import Backup, Recipe, Run, SavedRecipe, new_id, now


class Conflict(ValueError):
    """A stale page or another active run makes this action unsafe to repeat."""


class Store:
    def __init__(self, directory: str | Path):
        self.directory = Path(directory).expanduser().resolve()
        self.directory.mkdir(parents=True, exist_ok=True)
        self.path = self.directory / "studio.sqlite3"
        with self.connection() as db:
            db.execute("PRAGMA journal_mode=WAL")
            db.execute("CREATE TABLE IF NOT EXISTS recipes (id TEXT PRIMARY KEY, payload TEXT NOT NULL)")
            db.execute("CREATE TABLE IF NOT EXISTS runs (id TEXT PRIMARY KEY, state TEXT NOT NULL, updated TEXT NOT NULL, payload TEXT NOT NULL)")

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
            db.execute("INSERT INTO runs VALUES (?, ?, ?, ?)",
                       (run.id, run.state, run.updated_at, run.model_dump_json()))
        return run

    def get_run(self, run_id: str) -> Run:
        with self.connection() as db:
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

    def mutate(self, run_id: str, change: Callable[[Run], None], revision: int | None = None) -> Run:
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT payload FROM runs WHERE id = ?", (run_id,)).fetchone()
            if row is None:
                raise KeyError("That run was not found.")
            run = Run.model_validate_json(row[0])
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
            row = db.execute("SELECT payload FROM runs WHERE id = ?", (run_id,)).fetchone()
            if row is None:
                raise KeyError("That run was not found.")
            run = Run.model_validate_json(row[0])
            if run.revision != revision:
                raise Conflict("This run changed. Reload it before continuing.")
            if run.mode != "live" or run.state == "completed":
                raise Conflict("This run is already complete. Start a fresh run to use it again.")
            run.state, run.error, run.pause_requested = "running", "", False
            run.updated_at = now()
            run.revision += 1
            db.execute("UPDATE runs SET state = ?, updated = ?, payload = ? WHERE id = ?",
                       (run.state, run.updated_at, run.model_dump_json(), run.id))
        return run

    def recover(self) -> int:
        """Called only while holding the application's exclusive runtime lock."""
        recovered = 0
        for run in self.runs(limit=None):
            if run.state != "running":
                continue

            def interrupt(current):
                current.state = "interrupted"
                current.error = ("The app stopped during this step. Completed steps are safe. "
                                 "The provider may have processed the unfinished request; check its usage before retrying.")
                current.pause_requested = False

            self.mutate(run.id, interrupt)
            recovered += 1
        return recovered

    def backup(self) -> Backup:
        # One read transaction provides a consistent snapshot even during a run.
        with self.connection() as db:
            db.execute("BEGIN")
            recipes = [SavedRecipe.model_validate_json(row[0]) for row in db.execute("SELECT payload FROM recipes")]
            runs = [Run.model_validate_json(row[0]) for row in db.execute("SELECT payload FROM runs")]
        return Backup(recipes=recipes, runs=runs)

    def restore(self, raw: bytes) -> tuple[int, int]:
        if len(raw) > 10_000_000:
            raise ValueError("Choose a Studio JSON backup smaller than 10 MB.")
        backup = Backup.model_validate_json(raw)
        from .runner import validate_recipe
        for record in backup.recipes:
            validate_recipe(record.recipe)
        for run in backup.runs:
            validate_recipe(run.recipe)
        # Import adds records. Matching records are skipped; different records
        # with the same ID receive a fresh ID, so local work is never overwritten.
        counts = [0, 0]
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            for kind, records in enumerate((backup.recipes, backup.runs)):
                table = "recipes" if kind == 0 else "runs"
                for record in records:
                    if kind == 1:
                        if record.state == "running":
                            record.state = "interrupted"
                            record.error = "Restored during an unfinished step. Check provider usage before retrying it."
                        record.pause_requested = False
                    existing = db.execute(f"SELECT payload FROM {table} WHERE id = ?", (record.id,)).fetchone()
                    if existing and existing[0] == record.model_dump_json():
                        continue
                    if existing:
                        # Stable rekeying also deduplicates a repeated import
                        # after the first collision has been preserved.
                        record.id = hashlib.sha256(("studio-import-v1:" + record.model_dump_json()).encode()).hexdigest()[:32]
                        imported = db.execute(f"SELECT payload FROM {table} WHERE id = ?", (record.id,)).fetchone()
                        if imported and imported[0] == record.model_dump_json():
                            continue
                        if imported:
                            record.id = new_id()
                    if kind == 1:
                        db.execute("INSERT INTO runs VALUES (?, ?, ?, ?)",
                                   (record.id, record.state, record.updated_at, record.model_dump_json()))
                    else:
                        db.execute("INSERT INTO recipes VALUES (?, ?)", (record.id, record.model_dump_json()))
                    counts[kind] += 1
        return tuple(counts)
