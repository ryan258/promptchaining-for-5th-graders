"""Bounded execution with durable checkpoints and explicit, human retries."""

from concurrent.futures import ThreadPoolExecutor
import json
import logging
import re
from threading import Lock
from time import monotonic
from typing import Callable

from lib.core import llm_client
from .models import Recipe, Result, Run
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
        self.call = call or llm_client.prompt_once
        self.model_factory = model_factory or llm_client.build_models
        self.pool = ThreadPoolExecutor(max_workers=1, thread_name_prefix="studio")
        self.guard = Lock()
        self.lockfile = None
        self.closed = False

    def open(self):
        """One server owns recovery and provider execution for a workspace."""
        with self.guard:
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
            self.lockfile = handle
            self.store.recover()

    def start(self, run_id: str, revision: int):
        self.open()
        current = self.store.get_run(run_id)
        validate_recipe(current.recipe)
        client, names = self.model_factory()
        if current.model not in names:
            raise ValueError("This run's model is no longer configured. Reuse the recipe and choose a current model.")
        # Serializes claiming and scheduling with shutdown. SQLite guards tabs.
        with self.guard:
            if self.closed:
                raise Conflict("The app is shutting down. Restart it to continue.")
            run = self.store.claim(run_id, revision)
            return self.pool.submit(self._execute, run, (client, run.model))

    def _execute(self, run: Run, model):
        try:
            while len(run.results) < len(run.recipe.steps):
                # A pause always lets an already-dispatched step finish.
                rendered = render_prompt(run.recipe.steps[len(run.results)].prompt, run)
                started = monotonic()
                output, usage = self.call(model, rendered)
                if not isinstance(output, str) or not output.strip():
                    raise PromptError("The model returned an empty answer.")
                if len(output) > 60000:
                    raise PromptError("The answer was too large to save. Lower MAX_TOKENS and retry.")
                usage = usage or {}

                def count(name):
                    value = usage.get(name, 0) if isinstance(usage, dict) else getattr(usage, name, 0)
                    return max(0, int(value or 0))

                result = Result(prompt=rendered, output=output, prompt_tokens=count("prompt_tokens"),
                                completion_tokens=count("completion_tokens"), seconds=monotonic() - started)

                def checkpoint(current):
                    current.results.append(result)
                    if len(current.results) == len(current.recipe.steps):
                        current.state = "completed"
                    elif current.review_each or current.pause_requested:
                        current.state = "paused"
                    current.pause_requested = False

                run = self.store.mutate(run.id, checkpoint)
                if run.state != "running":
                    return
        except Exception as exc:
            # Deliberately log the type only: API exceptions can contain secrets.
            logger.warning("Studio step stopped (%s)", type(exc).__name__)
            message = str(exc) if isinstance(exc, PromptError) else error_message(exc)

            def fail(current):
                current.state, current.error, current.pause_requested = "failed", message, False

            self.store.mutate(run.id, fail)

    def pause(self, run_id: str) -> Run:
        def change(run):
            if run.state != "running":
                raise Conflict("This run is already stopped. Reload it to see the saved results.")
            run.pause_requested = True
        return self.store.mutate(run_id, change)

    def edit_last(self, run_id: str, output: str, revision: int) -> Run:
        if not output.strip() or len(output) > 60000:
            raise ValueError("The answer must contain 1–60,000 characters.")

        def change(run):
            if run.state not in {"paused", "failed", "interrupted"} or not run.results:
                raise Conflict("Only the last answer of a stopped, unfinished run can be edited.")
            if run.results[-1].original_output is None:
                run.results[-1].original_output = run.results[-1].output
            run.results[-1].output = output.strip()
            run.results[-1].edited = True
        return self.store.mutate(run_id, change, revision)

    def close(self):
        with self.guard:
            self.closed = True
            if self.lockfile is not None:
                for run in self.store.runs(limit=None):
                    if run.state == "running":
                        try:
                            self.pause(run.id)
                        except Conflict:
                            pass  # The worker finished between the read and pause.
        self.pool.shutdown(wait=True)
        if self.lockfile:
            self.lockfile.close()
            self.lockfile = None


def export_markdown(run: Run) -> str:
    lines = [f"# {run.topic}", "", f"Recipe: {run.recipe.title}", f"Audience: {run.recipe.audience}",
             f"Mode: {'Authored worked example — no AI calls' if run.mode == 'example' else 'AI-generated — review factual claims'}",
             f"Model: {run.model}", f"Status: {run.state}", f"Saved: {run.updated_at}", ""]
    if run.context:
        lines.extend(["## Context", "", run.context, ""])
    for index, result in enumerate(run.results):
        lines.extend([f"## {index + 1}. {run.recipe.steps[index].name}", "", result.output, ""])
        if result.edited:
            lines.extend(["*Edited by the author before continuing.*", ""])
    return "\n".join(lines)
