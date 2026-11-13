"""Plan and play a saved offline chain with answers supplied by people."""

import re

from .chain_lab_missions import CHAIN_LAB_MISSIONS
from .models import Recipe, Result, Run, Step
from .runner import OUTPUT, TOKEN, PromptError, render_prompt, validate_recipe
from .store import Conflict, Store

TEXT_LIMIT = 4000
MAX_STEPS = 5
_ATTACHMENT = re.compile(r"\[(Goal|Clues|Answer\s+[0-9]+)\]", re.IGNORECASE)


def new_lab(mission: str) -> Run:
    if mission:
        starter = CHAIN_LAB_MISSIONS[mission]
        recipe, topic, context = starter.recipe, starter.topic, starter.context
    else:
        recipe = Recipe(title="My own chain", audience="My partner", steps=[
            Step(name="Get ideas", prompt="Give me two ideas for this goal:\n{{topic}}"),
            Step(name="Make something", prompt="Pick one of these ideas and turn it into something we can try.\n{{output[-1]}}"),
        ])
        topic, context = "", ""
    return Run(recipe=recipe, topic=topic or "My chain idea", context=context, mode="lab", model="Human answers")


def _compile_prompt(prompt: str, index: int) -> str:
    if len(prompt) > TEXT_LIMIT:
        raise ValueError(f"Keep the prompt for step {index + 1} to {TEXT_LIMIT:,} characters or fewer.")
    if TOKEN.search(prompt):
        raise ValueError(f"In step {index + 1}, use [Goal], [Clues], or [Answer 1] to attach text.")

    def replace(match):
        attachment = match.group(1).lower()
        if attachment == "goal":
            return "{{topic}}"
        if attachment == "clues":
            return "{{context}}"
        answer = int(attachment.split()[1])
        if not 1 <= answer <= index:
            raise ValueError(f"Step {index + 1} can only use answers from earlier steps.")
        return "{{output[-%d]}}" % (index + 1 - answer)

    return _ATTACHMENT.sub(replace, prompt)


def plan_prompt(prompt: str, index: int) -> str:
    """Show numbered answers in the editor while storing portable recipe syntax."""
    def replace(match):
        token = match.group(1)
        if token == "topic":
            return "[Goal]"
        if token == "context":
            return "[Clues]"
        output = OUTPUT.fullmatch(token)
        if output and not output.group(2):
            return f"[Answer {index + 1 - int(output.group(1))}]"
        return match.group()

    return TOKEN.sub(replace, prompt)


def attached_answers(prompt: str, index: int) -> tuple[int, ...]:
    return tuple(dict.fromkeys(
        index + 1 - int(output.group(1))
        for token in TOKEN.finditer(prompt)
        if (output := OUTPUT.fullmatch(token.group(1)))
    ))


def _validate_prompt_sizes(run: Run):
    # A plan should fit even if every human answer uses the full text allowance.
    preview = run.model_copy(update={"results": []})
    full_answer = Result(prompt="", output="x" * TEXT_LIMIT)
    for index, step in enumerate(run.recipe.steps):
        try:
            render_prompt(step.prompt, preview)
        except PromptError as exc:
            raise ValueError(f"Use fewer repeated answers or clues in step {index + 1}.") from exc
        preview.results.append(full_answer)


def save_plan(store: Store, run_id: str, revision: int, *, topic: str, context: str,
              names: list[str], prompts: list[str], play: bool) -> Run:
    def save(run: Run):
        if run.mode != "lab" or run.archived or run.state != "ready":
            raise Conflict("Open an editable Chain Lab plan before changing the prompts.")
        if not 2 <= len(names) == len(prompts) <= MAX_STEPS:
            raise ValueError("Give your chain two to five prompts.")
        if not topic.strip() or len(topic) > 3000:
            raise ValueError("Give your chain a goal in 1–3,000 characters.")
        if len(context) > TEXT_LIMIT:
            raise ValueError(f"Keep your clues to {TEXT_LIMIT:,} characters or fewer.")

        steps = []
        for index, (name, prompt) in enumerate(zip(names, prompts)):
            name, prompt = name.strip(), prompt.strip()
            if not name and not prompt:
                continue
            if not prompt or index != len(steps):
                raise ValueError("Fill in the prompts in order before adding another step.")
            compiled = _compile_prompt(prompt, index)
            name = name or f"Step {index + 1}"
            earlier = run.recipe.steps[index] if index < len(run.recipe.steps) else None
            purpose = earlier.purpose if earlier and earlier.prompt == compiled and earlier.name == name else ""
            steps.append(Step(name=name, prompt=compiled, purpose=purpose))
        if len(steps) < 2:
            raise ValueError("Give your chain at least two prompts.")

        run.recipe = run.recipe.model_copy(update={"steps": steps})
        run.topic, run.context = topic.strip(), context.strip()
        validate_recipe(run.recipe)
        _validate_prompt_sizes(run)
        if play:
            run.state = "paused"

    return store.mutate(run_id, save, revision)


def save_answer(store: Store, run_id: str, revision: int, answer: str) -> Run:
    def save(run: Run):
        if run.mode != "lab" or run.archived or run.state != "paused":
            raise Conflict("Open an active step in the Chain Lab before saving an answer.")
        if not answer.strip() or len(answer) > TEXT_LIMIT:
            raise ValueError(f"Enter a human answer in 1–{TEXT_LIMIT:,} characters.")
        prompt = render_prompt(run.recipe.steps[len(run.results)].prompt, run)
        run.results.append(Result(prompt=prompt, output=answer.strip()))
        if len(run.results) == len(run.recipe.steps):
            run.state = "completed"

    return store.mutate(run_id, save, revision)
