"""Saved offline practice with authored answers and real prompt handoffs."""

from .classroom_cases import CLASSROOM_CASES, ChainBuildingCase, classroom_case_for_run
from .models import Recipe, Result, Run, Step
from .professional_cases import CASES as PROFESSIONAL_CASES
from .professional_cases import ProfessionalCase
from .runner import render_prompt
from .store import Conflict, Store

PRACTICE_CASES = {**CLASSROOM_CASES, **PROFESSIONAL_CASES}


def saved_practice_case(run: Run) -> ProfessionalCase | None:
    slug = run.practice_case
    if slug in CLASSROOM_CASES:
        return classroom_case_for_run(slug, run.context)
    return PRACTICE_CASES.get(slug)


def new_practice(case_slug: str) -> Run:
    case = PRACTICE_CASES[case_slug]
    recipe = Recipe(
        title=case.title, description=case.description, audience=case.audience,
        steps=[Step(name=name, purpose=purpose, prompt=prompt) for name, purpose, prompt in case.steps],
    )
    return Run(recipe=recipe, topic=case.topic, context=case.context, mode="practice",
               model="Authored practice", practice_case=case_slug)


def advance_practice(store: Store, run_id: str, revision: int) -> Run:
    def save_answer(run: Run):
        if run.archived:
            raise Conflict("Move this practice run out of the archive before continuing.")
        if run.mode != "practice" or run.state not in {"ready", "paused"}:
            raise Conflict("This practice step is already finished. Reload to see the saved answers.")
        case = saved_practice_case(run)
        if case is None:
            raise KeyError(run.practice_case)
        index = len(run.results)
        answer_count = len(case.outputs) + (1 if isinstance(case, ChainBuildingCase) else 0)
        if len(run.recipe.steps) != answer_count:
            raise ValueError("This practice recipe has changed. Open a new copy from the practice page.")
        if isinstance(case, ChainBuildingCase) and index == len(case.outputs):
            choice = case.choice_for(run.results[-1].output)
            if choice is None:
                raise ValueError("Pick a job for the final prompt first.")
            output = choice.example
        else:
            output = case.outputs[index]
        run.results.append(Result(prompt=render_prompt(run.recipe.steps[index].prompt, run),
                                  output=output))
        run.state = "completed" if len(run.results) == len(run.recipe.steps) else "paused"

    return store.mutate(run_id, save_answer, revision)
