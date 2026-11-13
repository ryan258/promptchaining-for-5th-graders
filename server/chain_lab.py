"""HTML entry points for the offline Chain Lab."""

import sqlite3
from types import SimpleNamespace

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import ValidationError
from starlette.concurrency import run_in_threadpool

from lib.core.llm_client import OPENROUTER_FREE_MODEL
from lib.workbench import chain_lab
from lib.workbench.chain_lab_missions import STARTER_MISSIONS
from lib.workbench.kid_insight_missions import KID_INSIGHT_MISSIONS
from lib.workbench.models import Run
from lib.workbench.runner import render_prompt
from lib.workbench.store import Conflict
from . import workbench

router = APIRouter()
TEMPLATE = "workbench/chain_lab.html"


def _open_run(run: Run):
    return RedirectResponse(f"/studio/runs/{run.id}", status_code=303)


@router.get("/studio/lab", response_class=HTMLResponse)
def missions(request: Request):
    return workbench.render(request, TEMPLATE, active="recipes", phase="choose",
                            missions=STARTER_MISSIONS, insight_missions=KID_INSIGHT_MISSIONS)


@router.post("/studio/lab")
async def start(request: Request):
    try:
        async with request.form() as form:
            mission = str(form.get("mission", ""))
        run = await run_in_threadpool(start_lab, mission)
        return _open_run(run)
    except (ValueError, KeyError, sqlite3.Error, OSError) as exc:
        return workbench.problem(request, exc)


def start_lab(mission: str):
    return workbench.get_store().create_run(chain_lab.new_lab(mission))


def render_lab(request: Request, run: Run, *, status: int = 200, error: str = "",
               values=None, answer: str = "", unsaved_answer: str = ""):
    step_index = len(run.results)
    complete = run.state == "completed"
    design = run.state == "ready" or values is not None
    next_prompt, attached = "", ()
    if not (complete or design or run.archived):
        template = run.recipe.steps[step_index].prompt
        try:
            next_prompt = render_prompt(template, run)
            attached = chain_lab.attached_answers(template, step_index)
        except ValueError as exc:
            error = error or str(exc)

    source_run = None
    if run.parent_run_id:
        try:
            source = workbench.get_store().get_run(run.parent_run_id)
            if source.mode == "lab":
                source_run = source
        except (KeyError, ValidationError):
            pass  # A run can be imported on its own.

    plan_prompts = values.step_prompt if values is not None else [
        chain_lab.plan_prompt(step.prompt, index) for index, step in enumerate(run.recipe.steps)
    ]
    reusable_answer = ""
    if source_run and next_prompt and step_index < len(source_run.results):
        previous = source_run.results[step_index]
        if previous.prompt == next_prompt and len(previous.output) <= chain_lab.TEXT_LIMIT:
            reusable_answer = previous.output
    return workbench.render(
        request, TEMPLATE, active="library", status=status, phase="design" if design else "play",
        run=run, source_run=source_run, next_prompt=next_prompt, attached_answers=attached,
        step_index=step_index, complete=complete, error=error, values=values,
        conflicted_plan=values is not None and (run.state != "ready" or run.archived),
        answer=answer, unsaved_answer=unsaved_answer, plan_prompts=plan_prompts,
        reusable_answer=reusable_answer,
        plan_saved=design and values is None and request.query_params.get("plan_saved") == "1",
        context_limit=chain_lab.TEXT_LIMIT, prompt_limit=chain_lab.TEXT_LIMIT, answer_limit=chain_lab.TEXT_LIMIT,
    )


def form_error(request: Request, run_id: str, exc: Exception, *, values=None, answer: str = ""):
    if isinstance(exc, KeyError):
        return workbench.problem(request, exc, run_id=run_id)
    run = workbench.get_run(run_id)
    if run.mode != "lab":
        return workbench.problem(request, exc, run_id=run_id)
    if isinstance(exc, (sqlite3.Error, OSError)):
        message, status = workbench.storage_message(), 503
    elif isinstance(exc, Conflict):
        message, status = str(exc), 409
    elif isinstance(exc, ValidationError):
        message, status = exc.errors(include_input=False)[0]["msg"], 400
    else:
        message, status = str(exc), 400
    keep_separate = bool(answer and (status == 409 or run.archived or run.state != "paused"))
    return render_lab(request, run, status=status, error=message, values=values,
                      answer="" if keep_separate else answer, unsaved_answer=answer if keep_separate else "")


@router.post("/studio/lab/{run_id}/plan")
async def plan(request: Request, run_id: str):
    values = None
    try:
        async with request.form() as form:
            values = SimpleNamespace(topic=str(form.get("topic", "")), context=str(form.get("context", "")),
                                     step_name=[str(name) for name in form.getlist("step_name")],
                                     step_prompt=[str(prompt) for prompt in form.getlist("step_prompt")])
            revision = int(form.get("revision", "-1"))
            action = form.get("action", "play")
        if action == "free-ai":
            live_run = await run_in_threadpool(prepare_free_lab_run, run_id, revision, values)
            return _open_run(live_run)
        if action not in {"play", "save"}:
            raise ValueError("Choose Play step 1, Save plan, or Prepare free AI run.")
        run = await run_in_threadpool(
            save_lab_plan, run_id, revision, values, action == "play",
        )
        if action == "save":
            return RedirectResponse(f"/studio/runs/{run.id}?plan_saved=1", status_code=303)
        return _open_run(run)
    except (ValueError, KeyError, sqlite3.Error, OSError) as exc:
        return await run_in_threadpool(form_error, request, run_id, exc, values=values)


def save_lab_plan(run_id: str, revision: int, values, play: bool):
    return chain_lab.save_plan(workbench.get_store(), run_id, revision,
                               topic=values.topic, context=values.context, names=values.step_name,
                               prompts=values.step_prompt, play=play)


def prepare_free_lab_run(run_id: str, revision: int, values) -> Run:
    config = workbench.configuration()
    if not config["ready"]:
        raise ValueError(config["error"] or "Add your OpenRouter API key to .env, then restart.")
    plan = save_lab_plan(run_id, revision, values, play=False)
    return workbench.get_store().create_run(Run(
        recipe=plan.recipe, topic=plan.topic, context=plan.context,
        model=OPENROUTER_FREE_MODEL, review_each=True,
    ))


@router.post("/studio/lab/{run_id}/answer")
async def answer_step(request: Request, run_id: str):
    answer = ""
    try:
        async with request.form() as form:
            answer = str(form.get("answer", ""))
            revision = int(form.get("revision", "-1"))
        run = await run_in_threadpool(save_lab_answer, run_id, revision, answer)
        return _open_run(run)
    except (ValueError, KeyError, sqlite3.Error, OSError) as exc:
        return await run_in_threadpool(form_error, request, run_id, exc, answer=answer)


def save_lab_answer(run_id: str, revision: int, answer: str):
    return chain_lab.save_answer(workbench.get_store(), run_id, revision, answer)


@router.post("/studio/lab/{run_id}/remix")
async def remix(request: Request, run_id: str):
    try:
        async with request.form() as form:
            revision = int(form.get("revision", "-1"))
        run = await run_in_threadpool(remix_lab, run_id, revision)
        return _open_run(run)
    except (ValueError, KeyError, sqlite3.Error, OSError) as exc:
        return await run_in_threadpool(form_error, request, run_id, exc)


def remix_lab(run_id: str, revision: int):
    store = workbench.get_store()
    if store.get_run(run_id).mode != "lab":
        raise Conflict("Choose a Chain Lab plan to remix.")
    return store.fork_run(run_id, 0, revision)
