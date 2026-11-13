"""Bounded execution with durable checkpoints and explicit, human retries."""

from concurrent.futures import ThreadPoolExecutor
import json
import logging
import re
import sqlite3
from threading import Lock
from time import monotonic
from typing import Callable

from lib.core import llm_client
from .classroom_cases import CHAIN_BUILDING_CASES
from .models import ModelSettings, Recipe, Result, Run, StepCheckpoint
from .store import Conflict, Store

logger = logging.getLogger(__name__)
TOKEN = re.compile(r"\{\{\s*([^{}]+?)\s*\}\}")
OUTPUT = re.compile(r"output\[-([1-8])\](?:\.([A-Za-z_][A-Za-z0-9_]*))?")


class PromptError(ValueError):
    """A safe-to-display error from our own prompt validation."""


def validate_recipe(recipe: Recipe) -> None:
    for index, step in enumerate(recipe.steps):
        for match in TOKEN.finditer(step.prompt):
            token = match.group(1)
            if token in {"topic", "context", "audience"}:
                continue
            output = OUTPUT.fullmatch(token)
            if not output:
                raise PromptError(f"Step {index + 1}: unknown placeholder {{{{{token}}}}}. Use topic, context, audience or output[-1].")
            if int(output.group(1)) > index:
                raise PromptError(f"Step {index + 1} refers to an answer that does not exist yet.")


def render_prompt(template: str, run: Run) -> str:
    """Substitute only the original template, never placeholders inside user data."""
    context = {"topic": run.topic, "context": run.context or "No additional context.", "audience": run.recipe.audience}

    def replace(match):
        token = match.group(1)
        if token in context:
            return context[token]
        output = OUTPUT.fullmatch(token)
        if not output or int(output.group(1)) > len(run.results):
            raise PromptError(f"Cannot resolve {{{{{token}}}}}. Check this step's prompt.")
        value = run.results[-int(output.group(1))].output
        if output.group(2):
            try:
                value = json.loads(value)[output.group(2)]
            except (ValueError, KeyError, TypeError) as exc:
                raise PromptError(f"The previous answer has no JSON field '{output.group(2)}'. Edit the answer or use the whole output.") from exc
        return value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)

    rendered = TOKEN.sub(replace, template)
    if len(rendered) > 120000:
        raise PromptError("This prompt is too large. Shorten the context or the previous answer before continuing.")
    return rendered


def error_message(exc: Exception) -> str:
    """Keep provider payloads, credentials and private URLs out of UI and logs."""
    from openai import AuthenticationError, RateLimitError, APITimeoutError, APIConnectionError, BadRequestError
    if isinstance(exc, AuthenticationError):
        return "OpenRouter did not accept the API key. Check OPENROUTER_API_KEY in .env, then restart the app."
    if isinstance(exc, RateLimitError):
        return "The provider reported a usage or rate limit. Check your OpenRouter account before retrying."
    if isinstance(exc, APITimeoutError):
        return "The provider timed out. It may have processed the request. Check usage before retrying this step."
    if isinstance(exc, APIConnectionError):
        return "Could not reach OpenRouter. Check your connection. The last completed step is saved."
    if isinstance(exc, BadRequestError):
        return "The provider rejected this request. Check the configured model, context size and token limit."
    return "This step could not be completed. Earlier answers are saved. Check your connection and model configuration before retrying."


class Runner:
    def __init__(self, store: Store, call: Callable | None = None, model_factory: Callable | None = None):
        self.store = store
        self.call = call or llm_client.request_completion
        self.model_factory = model_factory or llm_client.build_workbench_models
        self.pool = ThreadPoolExecutor(max_workers=1, thread_name_prefix="studio")
        self.guard = Lock()
        self.lockfile = None
        self.closed = False
        self.checkpoint: StepCheckpoint | None = None

    def open(self):
        """One server owns recovery and provider execution for a workspace."""
        with self.guard:
            if self.closed:
                raise Conflict("The app is shutting down. Restart it to continue.")
            if self.lockfile is not None:
                return
            handle = (self.store.directory / "runtime.lock").open("a+b")
            try:
                if __import__("os").name == "nt":
                    import msvcrt
                    handle.seek(0)
                    handle.write(b"0")
                    handle.flush()
                    handle.seek(0)
                    msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError as exc:
                handle.close()
                raise Conflict("This workspace is open in another server. Use that server or stop it first.") from exc
            try:
                self._recover_checkpoint()
                self.store.recover(preserve_run_id=self.checkpoint.run_id if self.checkpoint else None)
            except Exception:
                handle.close()
                raise
            self.lockfile = handle

    def _recover_checkpoint(self):
        try:
            self.checkpoint = self.store.read_pending_checkpoint()
        except (ValueError, OSError):
            self._preserve_pending_checkpoint()
            return
        if self.checkpoint is None:
            return
        try:
            self._flush_checkpoint()
        except (Conflict, KeyError):
            self._preserve_pending_checkpoint()
            self.checkpoint = None
        except (OSError, sqlite3.Error):
            logger.warning("A pending Studio checkpoint still needs a local save.")

    def _preserve_pending_checkpoint(self):
        try:
            self.store.preserve_pending_checkpoint()
        except OSError:
            logger.warning("Could not move an unreadable or unmatched Studio checkpoint.")
        else:
            logger.warning("Preserved an unreadable or unmatched Studio checkpoint in the workspace.")

    def start(self, run_id: str, revision: int):
        self.open()
        current = self.store.get_run(run_id)
        if current.mode != "live":
            raise Conflict("Only live runs can send a model request.")
        if current.archived:
            raise Conflict("Move this run out of the archive before continuing.")
        validate_recipe(current.recipe)
        client, names = self.model_factory()
        if current.model not in names:
            raise ValueError("This run's model is no longer configured. Reuse the recipe and choose a current model.")
        # Serializes claiming and scheduling with shutdown. SQLite guards tabs.
        with self.guard:
            if self.closed:
                raise Conflict("The app is shutting down. Restart it to continue.")
            if self.checkpoint is not None:
                raise Conflict("A run has an answer or status waiting to save. Retry the local save before starting a request.")
            run = self.store.claim(run_id, revision)
            return self.pool.submit(self._execute, run, (client, run.model))

    def _execute(self, run: Run, model):
        while run.state == "running":
            execution_id = run.execution_id
            attempt_id = None
            try:
                rendered = render_prompt(run.recipe.steps[len(run.results)].prompt, run)
                model_settings = self._model_settings()
                try:
                    with self.guard:
                        run = self.store.begin_step(run.id, execution_id, stop_before_dispatch=self.closed)
                except Conflict:
                    return
                if run.state != "running":
                    return
                attempt_id = run.active_attempt_id
                started = monotonic()
                response = self.call(model, rendered)
                result = self._result(response, rendered, attempt_id, monotonic() - started, model_settings)
                checkpoint = StepCheckpoint(
                    run_id=run.id, execution_id=execution_id, attempt_id=attempt_id, result=result,
                )
            except Exception as exc:
                # Deliberately log the type only: API exceptions can contain secrets.
                logger.warning("Studio step stopped (%s)", type(exc).__name__)
                message = str(exc) if isinstance(exc, PromptError) else error_message(exc)
                if not attempt_id and isinstance(exc, (OSError, sqlite3.Error)):
                    message = "The local database could not start this step. No model request was sent for it."
                checkpoint = StepCheckpoint(
                    run_id=run.id, execution_id=execution_id, attempt_id=attempt_id, error=message,
                )
            saved = self._record_checkpoint(checkpoint)
            if saved is None:
                return
            run = saved

    def _model_settings(self) -> ModelSettings | None:
        if self.call is not llm_client.request_completion:
            return None
        settings = llm_client.get_prompt_settings()
        return ModelSettings(max_tokens=settings["max_tokens"], temperature=settings["temperature"],
                             timeout_seconds=settings["timeout"])

    @staticmethod
    def _result(response, prompt, attempt_id, seconds, model_settings):
        provenance = {}
        if isinstance(response, llm_client.Completion):
            output, usage = response.text, response.usage
            for key, limit in (("finish_reason", 100), ("response_id", 200), ("response_model", 200)):
                value = getattr(response, key)
                if isinstance(value, str):
                    provenance[key] = value[:limit]
        else:
            output, usage = response  # Existing injected callables may return a tuple.
        if not isinstance(output, str) or not output.strip():
            raise PromptError("The model returned an empty answer.")
        if len(output) > 60000:
            raise PromptError("The answer was too large to save. Lower MAX_TOKENS and retry.")
        return Result(prompt=prompt, output=output, attempt_id=attempt_id, seconds=seconds,
                      model_settings=model_settings, **provenance, **llm_client.normalize_usage(usage))

    def _record_checkpoint(self, checkpoint: StepCheckpoint) -> Run | None:
        try:
            return self.store.finish_step(checkpoint)
        except Conflict:
            return None
        except (OSError, sqlite3.Error) as exc:
            logger.warning("Studio checkpoint needs a local save (%s)", type(exc).__name__)
            with self.guard:
                self.checkpoint = checkpoint
                try:
                    self.store.write_pending_checkpoint(checkpoint)
                except OSError:
                    logger.warning("The pending Studio checkpoint is held in memory. Keep the app open to retry its save.")
            return None

    def pending_save(self, run_id: str) -> bool:
        with self.guard:
            return self.checkpoint is not None and self.checkpoint.run_id == run_id

    def _flush_checkpoint(self) -> Run:
        checkpoint = self.checkpoint
        if checkpoint is None:
            raise Conflict("There is no pending local save.")
        run = self.store.finish_step(checkpoint, stop_after_save=True)
        self.checkpoint = None
        try:
            if self.store.read_pending_checkpoint() == checkpoint:
                self.store.pending_path.unlink(missing_ok=True)
        except (ValueError, OSError):
            logger.warning("Could not remove the saved Studio checkpoint journal.")
        return run

    def retry_save(self, run_id: str) -> Run:
        with self.guard:
            if self.checkpoint is None or self.checkpoint.run_id != run_id:
                raise Conflict("This run has no pending local save. Reload it to check the latest state.")
            return self._flush_checkpoint()

    def pause(self, run_id: str, execution_id: str | None = None) -> Run:
        def change(run):
            if run.state != "running":
                raise Conflict("This run is already stopped. Reload it to see the saved results.")
            if execution_id is not None and run.execution_id != execution_id:
                raise Conflict("This page refers to an earlier execution. Reload it before pausing.")
            run.pause_requested = True
        return self.store.mutate(run_id, change)

    def edit_last(self, run_id: str, output: str, revision: int) -> Run:
        if not output.strip() or len(output) > 60000:
            raise ValueError("The answer must contain 1–60,000 characters.")
        output = output.strip()

        def change(run):
            if run.archived:
                raise Conflict("Move this run out of the archive before editing it.")
            if run.state not in {"paused", "failed", "interrupted"} or not run.results:
                raise Conflict("Only the last answer of a stopped, unfinished run can be edited.")
            if run.mode == "lab":
                raise Conflict("Open the Chain Lab to save an answer or remix your plan.")
            if case := CHAIN_BUILDING_CASES.get(run.practice_case or ""):
                if len(run.results) != len(case.outputs) or case.choice_for(output) is None:
                    raise ValueError("Choose one of the two jobs shown in the challenge.")
            if run.results[-1].original_output is None:
                run.results[-1].original_output = run.results[-1].output
            run.results[-1].output = output
            run.results[-1].edited = True
        return self.store.mutate(run_id, change, revision)

    def close(self):
        with self.guard:
            self.closed = True
            if self.lockfile is not None:
                try:
                    for run_id in self.store.running_ids():
                        if self.checkpoint is None or self.checkpoint.run_id != run_id:
                            try:
                                self.pause(run_id)
                            except Conflict:
                                pass  # The worker finished between the read and pause.
                except (OSError, sqlite3.Error):
                    logger.warning("Could not write a Studio pause request during shutdown.")
        self.pool.shutdown(wait=True)
        with self.guard:
            if self.checkpoint is not None:
                try:
                    self._flush_checkpoint()
                except (Conflict, KeyError, OSError, sqlite3.Error):
                    logger.warning("A Studio checkpoint still needs a local save.")
        if self.lockfile:
            self.lockfile.close()
            self.lockfile = None


def export_markdown(run: Run) -> str:
    mode = {"example": "Authored worked example", "practice": "Authored practice run",
            "live": "AI-generated — review factual claims", "lab": "Human answers in the Chain Lab"}[run.mode]
    lines = [f"# {run.topic}", "", f"Recipe: {run.recipe.title}", f"Audience: {run.recipe.audience}",
             f"Mode: {mode}{' — no AI calls' if run.mode != 'live' else ''}",
             f"Model: {run.model}", f"Status: {run.state}", f"Saved: {run.updated_at}", ""]
    if run.context:
        lines.extend(["## Context", "", run.context, ""])
    for index, result in enumerate(run.results):
        lines.extend([f"## {index + 1}. {run.recipe.steps[index].name}", "", result.output, ""])
        if result.edited:
            lines.extend(["*Edited by the author before continuing.*", ""])
    return "\n".join(lines)
