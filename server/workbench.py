"""Thin HTML routes for the local workbench; execution and storage live in lib/."""

from functools import lru_cache
from pathlib import Path
import os
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from fastapi import APIRouter, HTTPException, Request, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from pydantic import ValidationError
from dotenv import load_dotenv

from lib.core.artifact_store import ArtifactStore
from lib.core.llm_client import configured_model_names, get_prompt_settings, has_api_key
from lib.workbench.models import Recipe, Run, Step
from lib.workbench.recipes import RECIPES, worked_example
from lib.workbench.runner import Runner, export_markdown, render_prompt, validate_recipe
from lib.workbench.store import Conflict, Store

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
        return {"ready": has_api_key(), "models": configured_model_names(),
                "max_tokens": settings["max_tokens"], "error": ""}
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
    except (ValueError, TypeError, ZoneInfoNotFoundError):
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
    elif isinstance(exc, ValidationError):
        errors = exc.errors(include_input=False, include_url=False)
        first = errors[0]
        field = " → ".join(str(part) for part in first["loc"])
        message, status = f"Check {field}: {first['msg']}", 400
    else:
        message, status = str(exc), 400
    return render(request, "workbench/error.html", status=status, message=message, run_id=run_id)


def get_run(run_id: str) -> Run:
    try:
        return get_store().get_run(run_id)
    except KeyError as exc:
        raise HTTPException(404, "Run not found") from exc


def recipe_from_form(form) -> Recipe:
    names, prompts, purposes = form.getlist("step_name"), form.getlist("step_prompt"), form.getlist("step_purpose")
    if not names or len(names) > 8 or not len(names) == len(prompts) == len(purposes):
        raise ValueError("A recipe needs 1–8 steps, each with a name and a prompt.")
    recipe = Recipe(title=form.get("title", ""), description=form.get("description", ""),
                    audience=form.get("audience", ""),
                    steps=[Step(name=n, prompt=p, purpose=why) for n, p, why in zip(names, prompts, purposes)])
    validate_recipe(recipe)
    return recipe


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    runs = get_store().runs(limit=4)
    active_run = next((r for r in get_store().runs(limit=None) if r.state != "completed"), None)
    return render(request, "workbench/home.html", runs=runs, resume=active_run, recipes=RECIPES)


@router.get("/studio/recipes", response_class=HTMLResponse)
def recipes(request: Request):
    return render(request, "workbench/recipes.html", active="recipes", recipes=RECIPES, saved=get_store().recipes())


@router.get("/studio/new", response_class=HTMLResponse)
def editor(request: Request, recipe: str = "explain", saved: str = "", reuse: str = ""):
    topic, context, source, is_custom, review_each = "", "", recipe, False, True
    try:
        if reuse:
            previous = get_store().get_run(reuse)
            spec, topic, context, source = previous.recipe, previous.topic, previous.context, f"run-{reuse}"
            review_each = previous.review_each
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
                  saved_notice=request.query_params.get("saved_ok") == "1")


@router.post("/studio/prepare")
async def prepare(request: Request):
    form = await request.form(max_fields=50)
    try:
        recipe = recipe_from_form(form)
        if form.get("action") == "save":
            saved = get_store().save_recipe(recipe, str(form.get("topic", "")), str(form.get("context", "")),
                                            form.get("review_each") == "on")
            return RedirectResponse(f"/studio/new?saved={saved.id}&saved_ok=1", status_code=303)
        if form.get("action") != "run":
            raise ValueError("Choose Save recipe or Start chain.")
        config = configuration()
        if not config["ready"]:
            raise ValueError("Add your OpenRouter key and model to .env, then restart. You can still save recipes and open the worked example.")
        model = str(form.get("model", ""))
        if model not in config["models"]:
            raise ValueError("Choose one of your configured models.")
        topic = str(form.get("topic", "")).strip()
        if not topic:
            raise ValueError("Tell the chain what you want to work on.")
        run = Run(recipe=recipe, topic=topic, context=str(form.get("context", "")),
                  model=model, review_each=form.get("review_each") == "on")
        run = get_store().create_run(run)
        # A ready run is saved first. Its own page asks to dispatch the first call.
        return RedirectResponse(f"/studio/runs/{run.id}", status_code=303)
    except (ValueError, KeyError) as exc:
        return problem(request, exc)


@router.post("/studio/example")
def example():
    # One click opens the same local example instead of filling the library with copies.
    for run in get_store().runs(limit=None):
        if run.mode == "example":
            return RedirectResponse(f"/studio/runs/{run.id}", status_code=303)
    run = get_store().create_run(worked_example())
    return RedirectResponse(f"/studio/runs/{run.id}", status_code=303)


def run_context(run: Run) -> dict:
    preview, preview_error = "", ""
    if run.state != "completed":
        try:
            preview = render_prompt(run.recipe.steps[len(run.results)].prompt, run)
        except ValueError as exc:
            preview_error = str(exc)
    return {"run": run, "next_prompt": preview, "preview_error": preview_error}


@router.get("/studio/runs/{run_id}", response_class=HTMLResponse)
def run_page(request: Request, run_id: str):
    return render(request, "workbench/run.html", active="library", **run_context(get_run(run_id)))


@router.get("/studio/runs/{run_id}/status", response_class=HTMLResponse)
def run_status(request: Request, run_id: str):
    return render(request, "workbench/_run.html", **run_context(get_run(run_id)))


@router.post("/studio/runs/{run_id}/continue")
async def continue_run(request: Request, run_id: str):
    try:
        form = await request.form()
        get_runner().start(run_id, int(form.get("revision", "-1")))
        return RedirectResponse(f"/studio/runs/{run_id}", status_code=303)
    except (ValueError, KeyError) as exc:
        return problem(request, exc, run_id=run_id)


@router.post("/studio/runs/{run_id}/pause")
def pause_run(request: Request, run_id: str):
    try:
        get_runner().pause(run_id)
        return RedirectResponse(f"/studio/runs/{run_id}", status_code=303)
    except (ValueError, KeyError) as exc:
        return problem(request, exc, run_id=run_id)


@router.post("/studio/runs/{run_id}/edit")
async def edit_answer(request: Request, run_id: str):
    try:
        form = await request.form()
        get_runner().edit_last(run_id, str(form.get("output", "")), int(form.get("revision", "-1")))
        return RedirectResponse(f"/studio/runs/{run_id}", status_code=303)
    except (ValueError, KeyError) as exc:
        return problem(request, exc, run_id=run_id)


@router.get("/studio/runs/{run_id}/export")
def export_run(run_id: str, format: str = "markdown"):
    run = get_run(run_id)
    if format == "json":
        from lib.workbench.models import Backup
        data = Backup(runs=[run]).model_dump_json(indent=2)
        suffix, media = "json", "application/json"
    elif format == "markdown":
        data, suffix, media = export_markdown(run), "md", "text/markdown"
    else:
        raise HTTPException(400, "Choose markdown or json")
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
def library(request: Request, q: str = ""):
    if len(q) > 200:
        q = q[:200]
    return render(request, "workbench/library.html", active="library", runs=get_store().runs(q, limit=None), query=q,
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
async def restore(request: Request, backup_file: UploadFile = File(...)):
    try:
        from lib.workbench.backups import ARCHIVE_LIMIT
        raw = await backup_file.read(ARCHIVE_LIMIT + 1)
        from starlette.concurrency import run_in_threadpool
        recipes, runs = await run_in_threadpool(get_store().restore, raw)
        return RedirectResponse(f"/studio/library?restored={recipes}+recipes+and+{runs}+runs+added", status_code=303)
    except (ValueError, KeyError) as exc:
        return problem(request, exc)
    finally:
        await backup_file.close()


@router.get("/studio/learn", response_class=HTMLResponse)
def learn(request: Request):
    return render(request, "workbench/learn.html", active="learn")


@router.get("/studio/advanced", response_class=HTMLResponse)
def advanced(request: Request):
    return render(request, "workbench/advanced.html", active="advanced")
