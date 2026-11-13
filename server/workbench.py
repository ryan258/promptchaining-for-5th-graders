"""Thin HTML routes for the local workbench; execution and storage live in lib/."""

from functools import lru_cache
from pathlib import Path
import os
import sqlite3
from types import SimpleNamespace
from urllib.parse import urlencode
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from starlette.concurrency import run_in_threadpool
from starlette.datastructures import UploadFile
from starlette.formparsers import MultiPartException, MultiPartParser
from pydantic import ValidationError
from dotenv import load_dotenv

from lib.core.artifact_store import ArtifactStore
from lib.core.llm_client import OPENROUTER_FREE_MODEL, configured_model_names, get_prompt_settings, has_api_key
from lib.workbench.everyday_recipes import EVERYDAY_RECIPES
from lib.workbench.models import Recipe, Run, Step
from lib.workbench.backups import ARCHIVE_LIMIT
from lib.workbench.exports import final_markdown, starter_chat_prompt, trace_markdown
from lib.workbench.parent_insight_recipes import PARENT_INSIGHT_RECIPES
from lib.workbench.recipes import PARENT_RECIPES, RECIPES, RECIPE_EXAMPLES, RECIPE_INPUT_HINTS, worked_example
from lib.workbench.runner import Runner, export_markdown, render_prompt, validate_recipe
from lib.workbench.store import Conflict, Store
from lib.workbench.teacher_insight_recipes import TEACHER_INSIGHT_RECIPES
from lib.workbench.teacher_recipes import TEACHER_RECIPES

ROOT = Path(__file__).resolve().parents[1]
router = APIRouter()


@lru_cache(maxsize=1)
def get_store() -> Store:
    # Resolve the workspace only after reading .env. Merely starting the
    # app must not cache the default directory ahead of this setting.
    load_dotenv(ROOT / ".env")
    return Store(os.getenv("PROMPT_STUDIO_DATA", str(ROOT / "workspace")))


@lru_cache(maxsize=1)
def get_runner() -> Runner:
    runner = Runner(get_store())
    runner.open()
    return runner


def close_workbench():
    if get_runner.cache_info().currsize:
        get_runner().close()
    get_runner.cache_clear()
    get_store.cache_clear()


NAV = [
    ("home", "Workbench", "/"),
    ("recipes", "Recipes", "/studio/recipes"),
    ("library", "My library", "/studio/library"),
    ("learn", "Guides", "/studio/guides"),
    ("advanced", "Advanced", "/studio/advanced"),
]


def configuration() -> dict:
    try:
        settings = get_prompt_settings()
        return {"ready": has_api_key(), "models": configured_model_names(for_workbench=True),
                "free_model": OPENROUTER_FREE_MODEL, "max_tokens": settings["max_tokens"], "error": ""}
    except (ValueError, TypeError):
        return {"ready": False, "models": (), "max_tokens": 0,
                "error": "Check model IDs and numeric settings in .env, then restart the app."}


def local_date(value: str) -> str:
    try:
        stamp = datetime.fromisoformat(value)
        if stamp.tzinfo is None:
            return "Date unavailable"
        zone = ZoneInfo(os.getenv("STUDIO_TIMEZONE", "America/Chicago"))
        return stamp.astimezone(zone).strftime("%b %d, %Y").replace(" 0", " ")
    except (ValueError, TypeError, OverflowError, ZoneInfoNotFoundError):
        return "Date unavailable"


def render(request: Request, template: str, *, status: int = 200, active: str = "home", **context):
    return request.app.state.templates.TemplateResponse(
        request, template,
        {"title": "Prompt Chaining Studio", "active_page": active,
         "nav_items": [{"label": label, "href": href, "active": key == active} for key, label, href in NAV],
         "config": configuration(), **context}, status_code=status,
    )


def problem(request: Request, exc: Exception, *, run_id: str = ""):
    if isinstance(exc, KeyError):
        message, status = "That saved item was not found. Open your library to find your other work.", 404
    elif isinstance(exc, Conflict):
        message, status = str(exc), 409
    elif isinstance(exc, (sqlite3.Error, OSError)):
        message, status = storage_message(), 503
    elif isinstance(exc, ValidationError):
        errors = exc.errors(include_input=False, include_url=False)
        first = errors[0]
        field = " → ".join(str(part) for part in first["loc"])
        message, status = f"Check {field}: {first['msg']}", 400
    else:
        message, status = str(exc), 400
    return render(request, "workbench/error.html", status=status, message=message, run_id=run_id)


def storage_message() -> str:
    return "Studio could not write to the workspace. Check available disk space and try again."


def get_run(run_id: str) -> Run:
    try:
        return get_store().get_run(run_id)
    except KeyError as exc:
        raise HTTPException(404, "Run not found") from exc
    except ValidationError:
        raise HTTPException(422, "This saved run is unreadable. Preserve a stopped workspace-folder copy.") from None


def recipe_fields(form) -> dict:
    names, prompts, purposes = form.getlist("step_name"), form.getlist("step_prompt"), form.getlist("step_purpose")
    if not names or len(names) > 8 or not len(names) == len(prompts) == len(purposes):
        raise ValueError("A recipe needs 1–8 steps, each with a name and a prompt.")
    return {"title": form.get("title", ""), "description": form.get("description", ""),
            "audience": form.get("audience", ""),
            "steps": [{"name": name, "prompt": prompt, "purpose": purpose}
                      for name, prompt, purpose in zip(names, prompts, purposes)]}


def recipe_from_form(form) -> Recipe:
    recipe = Recipe.model_validate(recipe_fields(form))
    validate_recipe(recipe)
    return recipe


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    store = get_store()
    return render(request, "workbench/home.html", runs=store.run_summaries(limit=4),
                  resume=store.resume_run(), recipes=RECIPES,
                  everyday_recipes=EVERYDAY_RECIPES, teacher_recipes=TEACHER_RECIPES)


@router.get("/studio/recipes", response_class=HTMLResponse)
def recipes(request: Request):
    grouped = (PARENT_RECIPES.keys() | EVERYDAY_RECIPES.keys() | TEACHER_RECIPES.keys()
               | PARENT_INSIGHT_RECIPES.keys() | TEACHER_INSIGHT_RECIPES.keys())
    general = {key: recipe for key, recipe in RECIPES.items() if key not in grouped}
    return render(request, "workbench/recipes.html", active="recipes", recipes=general,
                  parent_recipes=PARENT_RECIPES, everyday_recipes=EVERYDAY_RECIPES,
                  teacher_recipes=TEACHER_RECIPES, parent_insight_recipes=PARENT_INSIGHT_RECIPES,
                  teacher_insight_recipes=TEACHER_INSIGHT_RECIPES, saved=get_store().recipes())


def recipe_starter_context(source: str) -> dict:
    hint = RECIPE_INPUT_HINTS.get(source)
    return {
        "topic_example": RECIPE_EXAMPLES.get(source),
        "input_hint": hint,
        "starter_prompt": starter_chat_prompt(RECIPES[source], hint) if hint else None,
    }


@router.get("/studio/new", response_class=HTMLResponse)
def editor(request: Request, recipe: str = "explain", saved: str = "", reuse: str = ""):
    topic, context, source, is_custom, review_each = "", "", recipe, False, True
    selected_model = ""
    try:
        if reuse:
            previous = get_store().get_run(reuse)
            spec, topic, context, source = previous.recipe, previous.topic, previous.context, f"run-{reuse}"
            review_each = previous.review_each
            selected_model = previous.model
        elif saved:
            item = get_store().get_recipe(saved)
            spec, topic, context, source, is_custom = item.recipe, item.topic, item.context, saved, True
            review_each = item.review_each
        elif recipe == "blank":
            spec = Recipe(title="My new chain", audience="Me; use plain language",
                          steps=[Step(name="Start here", prompt="Help {{audience}} with {{topic}}. Context: {{context}}.")])
        elif recipe in RECIPES:
            spec = RECIPES[recipe]
        else:
            raise KeyError(recipe)
    except KeyError as exc:
        return problem(request, exc)
    return render(request, "workbench/editor.html", active="recipes", recipe=spec, topic=topic,
                  context=context, source=source, is_custom=is_custom, review_each=review_each,
                  selected_model=selected_model, saved_notice=request.query_params.get("saved_ok") == "1",
                  **recipe_starter_context(source))


@router.post("/studio/prepare")
async def prepare(request: Request):
    async with request.form(max_fields=50, max_files=0) as form:
        return await run_in_threadpool(prepare_recipe, request, form)


def prepare_recipe(request: Request, form):
    try:
        recipe = recipe_from_form(form)
        topic, context = str(form.get("topic", "")), str(form.get("context", ""))
        if not topic.strip() and context.strip() and str(form.get("source", "")) in RECIPE_INPUT_HINTS:
            topic = recipe.title
        if form.get("action") == "save":
            saved = get_store().save_recipe(recipe, topic, context, form.get("review_each") == "on")
            return RedirectResponse(f"/studio/new?saved={saved.id}&saved_ok=1", status_code=303)
        if form.get("action") != "run":
            raise ValueError("Choose Save recipe or Start chain.")
        config = configuration()
        if not config["ready"]:
            raise ValueError(config["error"] or "Add your OpenRouter API key to .env, then restart. You can still save recipes.")
        model = str(form.get("model", ""))
        if model not in config["models"]:
            raise ValueError("Choose one of your configured models.")
        topic = topic.strip()
        if not topic:
            raise ValueError("Tell the chain what you want to work on.")
        run = Run(recipe=recipe, topic=topic, context=context,
                  model=model, review_each=form.get("review_each") == "on")
        run = get_store().create_run(run)
        # A ready run is saved first. Its own page asks to dispatch the first call.
        return RedirectResponse(f"/studio/runs/{run.id}", status_code=303)
    except (ValueError, KeyError, sqlite3.Error, OSError) as exc:
        return editor_error(request, form, exc)


def editor_error(request: Request, form, exc: Exception):
    try:
        data = recipe_fields(form)
    except ValueError:
        return problem(request, exc)
    field = ""
    if isinstance(exc, ValidationError):
        error = exc.errors(include_input=False, include_url=False)[0]
        location = error["loc"]
        field = str(location[0]) if location else ""
        if len(location) > 2 and field == "steps":
            field = f"step-{location[1]}-{location[2]}"
        message, status = error["msg"], 400
    elif isinstance(exc, (sqlite3.Error, OSError)):
        message, status = storage_message(), 503
    else:
        message, status = str(exc), 400
    if message.startswith("Step "):
        step_number = message.removeprefix("Step ").partition(" ")[0].rstrip(":")
        if step_number.isdecimal():
            field = f"step-{int(step_number) - 1}-prompt"
    if message == "Tell the chain what you want to work on.":
        field = "topic"
    source = str(form.get("source", "blank"))[:64]
    return render(
        request, "workbench/editor.html", active="recipes", status=status, recipe=SimpleNamespace(**data),
        topic=form.get("topic", ""), context=form.get("context", ""), source=source,
        is_custom=form.get("custom") == "1", review_each=form.get("review_each") == "on",
        selected_model=form.get("model", ""), form_error=message, error_field=field,
        **recipe_starter_context(source),
    )


@router.post("/studio/example")
def example(request: Request):
    try:
        run = get_store().open_example(worked_example)
    except (sqlite3.Error, OSError) as exc:
        return problem(request, exc)
    return RedirectResponse(f"/studio/runs/{run.id}", status_code=303)


@router.get("/studio/practice", response_class=HTMLResponse)
def practice_cases(request: Request):
    from lib.workbench.classroom_cases import CHAIN_BUILDING_CASES, CLASSROOM_CASES, PARENT_CASES

    general = {slug: case for slug, case in CLASSROOM_CASES.items()
               if slug not in PARENT_CASES and slug not in CHAIN_BUILDING_CASES}
    return render(request, "workbench/practice.html", active="recipes", cases=general,
                  parent_cases=PARENT_CASES, chain_building_cases=CHAIN_BUILDING_CASES)


@router.get("/studio/practice/professional", response_class=HTMLResponse)
def professional_cases(request: Request):
    from lib.workbench.professional_cases import CASES

    return render(request, "workbench/practice.html", active="recipes", cases=CASES, professional=True)


@router.post("/studio/practice/{case_slug}")
def start_practice(request: Request, case_slug: str):
    from lib.workbench.practice import new_practice

    try:
        run = get_store().create_run(new_practice(case_slug))
    except (KeyError, ValueError, sqlite3.Error, OSError) as exc:
        return problem(request, exc)
    return RedirectResponse(f"/studio/runs/{run.id}", status_code=303)


def run_context(run: Run) -> dict:
    preview, preview_error = "", ""
    if run.state != "completed":
        try:
            preview = render_prompt(run.recipe.steps[len(run.results)].prompt, run)
        except ValueError as exc:
            preview_error = str(exc)
    pending = bool(get_runner.cache_info().currsize and get_runner().pending_save(run.id))
    case = None
    classroom = False
    chain_case, prompt_choice = None, None
    if run.mode == "practice":
        from lib.workbench.classroom_cases import CLASSROOM_CASES, ChainBuildingCase
        from lib.workbench.practice import saved_practice_case

        case = saved_practice_case(run)
        classroom = run.practice_case in CLASSROOM_CASES
        if isinstance(case, ChainBuildingCase):
            chain_case = case
            if len(run.results) >= 2:
                prompt_choice = case.choice_for(run.results[1].output)
    return {"run": run, "next_prompt": preview, "preview_error": preview_error,
            "pending_save": pending, "practice_case": case, "classroom": classroom,
            "chain_case": chain_case, "prompt_choice": prompt_choice,
            "related_recipe": run.practice_case if classroom and run.practice_case in PARENT_RECIPES else None}


def render_run(request: Request, run: Run, *, status: int = 200, **extra):
    if run.mode == "lab":
        from .chain_lab import render_lab

        return render_lab(request, run, status=status, error=extra.get("edit_error", ""),
                          unsaved_answer=extra.get("submitted_edit", ""))
    context = run_context(run)
    template = "workbench/classroom_run.html" if context["classroom"] else "workbench/run.html"
    return render(request, template, active="library", status=status, **context, **extra)


@router.get("/studio/runs/{run_id}", response_class=HTMLResponse)
def run_page(request: Request, run_id: str):
    return render_run(request, get_run(run_id))


@router.get("/studio/runs/{run_id}/status", response_class=HTMLResponse)
def run_status(request: Request, run_id: str, revision: int | None = None, pending: bool = False):
    run = get_run(run_id)
    if run.mode == "lab":
        return Response(status_code=204)
    context = run_context(run)
    if context["run"].revision == revision and context["pending_save"] == pending:
        return Response(status_code=204)
    template = "workbench/_classroom.html" if context["classroom"] else "workbench/_run.html"
    return render(request, template, **context)


@router.post("/studio/runs/{run_id}/continue")
async def continue_run(request: Request, run_id: str):
    try:
        async with request.form() as form:
            await run_in_threadpool(advance_run, run_id, int(form.get("revision", "-1")))
        return RedirectResponse(f"/studio/runs/{run_id}", status_code=303)
    except (ValueError, KeyError, sqlite3.Error, OSError) as exc:
        return problem(request, exc, run_id=run_id)


def advance_run(run_id: str, revision: int):
    store = get_store()
    mode = store.get_run(run_id).mode
    if mode == "lab":
        raise Conflict("Open the Chain Lab and enter a human answer to continue.")
    if mode == "practice":
        from lib.workbench.practice import advance_practice

        advance_practice(store, run_id, revision)
    else:
        config = configuration()
        if not config["ready"]:
            raise ValueError(config["error"] or "Add your OpenRouter API key to .env, then restart.")
        get_runner().start(run_id, revision)


@router.post("/studio/runs/{run_id}/pause")
async def pause_run(request: Request, run_id: str):
    try:
        async with request.form() as form:
            await run_in_threadpool(pause_live_run, run_id, form.get("execution_id"))
        return RedirectResponse(f"/studio/runs/{run_id}", status_code=303)
    except (ValueError, KeyError, sqlite3.Error, OSError) as exc:
        return problem(request, exc, run_id=run_id)


def pause_live_run(run_id: str, execution_id: str | None):
    get_runner().pause(run_id, execution_id=execution_id)


@router.post("/studio/runs/{run_id}/retry-save")
def retry_save(request: Request, run_id: str):
    try:
        get_runner().retry_save(run_id)
    except (ValueError, KeyError, sqlite3.Error, OSError) as exc:
        return problem(request, exc, run_id=run_id)
    return RedirectResponse(f"/studio/runs/{run_id}", status_code=303)


@router.post("/studio/runs/{run_id}/organize")
async def organize_run(request: Request, run_id: str):
    async with request.form() as form:
        try:
            destination = await run_in_threadpool(update_run_organization, run_id, form)
        except (ValueError, KeyError, sqlite3.Error, OSError) as exc:
            return problem(request, exc, run_id=run_id)
    return RedirectResponse(f"/studio/runs/{destination}", status_code=303)


def update_run_organization(run_id: str, form) -> str:
    store = get_store()
    revision = int(form.get("revision", "-1"))
    action = form.get("action")
    if action == "note":
        store.set_resume_note(run_id, str(form.get("note", "")), revision)
    elif action in {"archive", "unarchive"}:
        store.set_archived(run_id, action == "archive", revision)
    elif action == "fork":
        return store.fork_run(run_id, int(form.get("step_count", "0")), revision).id
    else:
        raise ValueError("Choose a run action.")
    return run_id


@router.post("/studio/runs/{run_id}/edit")
async def edit_answer(request: Request, run_id: str):
    output = ""
    try:
        async with request.form() as form:
            output, revision = str(form.get("output", "")), int(form.get("revision", "-1"))
            await run_in_threadpool(save_edit, run_id, output, revision)
        return RedirectResponse(f"/studio/runs/{run_id}", status_code=303)
    except (ValueError, KeyError, sqlite3.Error, OSError) as exc:
        return await run_in_threadpool(edit_error, request, run_id, output, exc)


def save_edit(run_id: str, output: str, revision: int):
    get_runner().edit_last(run_id, output, revision)


def edit_error(request: Request, run_id: str, output: str, exc: Exception):
    if isinstance(exc, (KeyError, sqlite3.Error, OSError)):
        return problem(request, exc, run_id=run_id)
    return render_run(request, get_run(run_id),
                  status=409 if isinstance(exc, Conflict) else 400,
                  edit_error=str(exc), submitted_edit=output)


@router.get("/studio/runs/{run_id}/export")
def export_run(run_id: str, format: str = "markdown"):
    run = get_run(run_id)
    if format == "json":
        from lib.workbench.models import Backup
        data = Backup(runs=[run]).model_dump_json(indent=2)
        suffix, media = "json", "application/json"
    elif format == "markdown":
        data, suffix, media = export_markdown(run), "md", "text/markdown"
    elif format == "trace":
        data, suffix, media = trace_markdown(run), "trace.md", "text/markdown"
    elif format == "final":
        if run.state != "completed":
            raise HTTPException(409, "Finish this chain before downloading a final answer.")
        data, suffix, media = final_markdown(run), "final.md", "text/markdown"
    else:
        raise HTTPException(400, "Choose markdown, trace, final, or json.")
    return Response(data, media_type=media, headers={"Content-Disposition": f'attachment; filename="chain-{run.id[:8]}.{suffix}"'})


@router.post("/studio/runs/{run_id}/artifact")
def save_artifact(request: Request, run_id: str):
    run = get_run(run_id)
    if run.state != "completed":
        return problem(request, ValueError("Finish this chain before saving the final artifact."), run_id=run_id)
    try:
        store = ArtifactStore(base_dir=str(ROOT / "artifacts"))
        store.save(f"studio_{run.id}", "final", run.results[-1].output,
                   metadata={"tool": "prompt_chaining_studio", "run_id": run.id, "model": run.model, "mode": run.mode,
                             "topic": run.topic, "recipe": run.recipe.title})
    except (OSError, ValueError):
        return problem(request, ValueError("The artifact folder could not be updated. Your answer is still saved in this run; you can export it here."), run_id=run_id)
    return RedirectResponse(f"/studio/runs/{run.id}?artifact_saved=1", status_code=303)


@router.get("/studio/library", response_class=HTMLResponse)
def library(request: Request, q: str = "", page: int = 1, archived: bool = False):
    q = q[:200]
    page = max(1, min(page, 100_000))
    page_size = 30
    runs = get_store().run_summaries(q, limit=page_size + 1, offset=(page - 1) * page_size, archived=archived)
    def page_link(number):
        return "/studio/library?" + urlencode({"q": q, "page": number, "archived": str(archived).lower()})
    return render(request, "workbench/library.html", active="library", runs=runs[:page_size], query=q,
                  archived=archived,
                  previous_page=page_link(page - 1) if page > 1 else "",
                  next_page=page_link(page + 1) if len(runs) > page_size else "",
                  notice=request.query_params.get("restored", ""))


@router.get("/studio/backup")
def backup():
    try:
        data = get_store().archive()
    except (ValueError, OSError):
        raise HTTPException(400, "Backup could not be created. Preserve a stopped workspace-folder copy; existing work is unchanged.") from None
    return Response(data, media_type="application/zip",
                    headers={"Content-Disposition": 'attachment; filename="prompt-studio-backup.zip"'})


@router.post("/studio/restore")
async def restore(request: Request):
    # Limit the multipart envelope before the parser spools it to disk.
    if request.headers.get("content-type", "").split(";", 1)[0].strip().lower() != "multipart/form-data":
        return problem(request, ValueError("Choose a Studio backup file."))
    try:
        upload_limit = ARCHIVE_LIMIT + 16_384
        if int(request.headers.get("content-length", "0")) > upload_limit:
            raise BackupUploadTooLarge()
        form = await MultiPartParser(request.headers, bounded_backup_stream(request, upload_limit),
                                     max_files=1, max_fields=0).parse()
        try:
            backup_file = form.get("backup_file")
            if not isinstance(backup_file, UploadFile):
                raise ValueError("Choose a Studio backup file.")
            raw = await backup_file.read(ARCHIVE_LIMIT + 1)
            if len(raw) > ARCHIVE_LIMIT:
                raise BackupUploadTooLarge()
            recipes, runs = await run_in_threadpool(restore_bytes, raw)
        finally:
            await form.close()
        return RedirectResponse(f"/studio/library?restored={recipes}+recipes+and+{runs}+runs+added", status_code=303)
    except BackupUploadTooLarge:
        return render(request, "workbench/error.html", status=413,
                      message="Choose a Studio ZIP up to 128 MB or JSON up to 10 MB.", run_id="")
    except MultiPartException:
        return problem(request, ValueError("Upload one Studio backup file."))
    except (ValueError, KeyError, sqlite3.Error, OSError) as exc:
        return problem(request, exc)


class BackupUploadTooLarge(MultiPartException):
    def __init__(self):
        super().__init__("Backup upload exceeds its size limit.")


async def bounded_backup_stream(request: Request, limit: int):
    received = 0
    async for chunk in request.stream():
        received += len(chunk)
        if received > limit:
            raise BackupUploadTooLarge()
        yield chunk


def restore_bytes(raw: bytes):
    return get_store().restore(raw)


@router.get("/studio/learn", response_class=HTMLResponse)
def learn(request: Request):
    return render(request, "workbench/learn.html", active="learn")


@router.get("/studio/advanced", response_class=HTMLResponse)
def advanced(request: Request):
    return render(request, "workbench/advanced.html", active="advanced")
