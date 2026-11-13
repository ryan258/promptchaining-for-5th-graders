"""Deterministic examples for the workbench and portable chain API."""

import argparse

from lib.core.chain import MinimalChainable
from lib.workbench.classroom_cases import ChainBuildingCase
from lib.workbench.models import Result
from lib.workbench.practice import PRACTICE_CASES, new_practice
from lib.workbench.recipes import worked_example
from lib.workbench.runner import render_prompt, validate_recipe


def verify_workbench_examples():
    example = worked_example()
    if len(example.results) != 4 or example.results[0].output not in example.results[1].prompt:
        raise RuntimeError("The Moon fixture did not carry its first answer into step two.")

    for slug, case in PRACTICE_CASES.items():
        run = new_practice(slug)
        recipe = run.recipe
        validate_recipe(recipe)
        expected_outputs = 2 if isinstance(case, ChainBuildingCase) else 3
        if len(recipe.steps) != 3 or len(case.outputs) != expected_outputs or not case.rubric:
            raise RuntimeError(f"{case.title} needs three steps, prepared answers, and a rubric.")
        for step, output in zip(recipe.steps[:2], case.outputs[:2]):
            run.results.append(Result(prompt=render_prompt(step.prompt, run), output=output))
        if isinstance(case, ChainBuildingCase):
            revisions = [choice.instruction for choice in case.choices]
            source = run.results[0].output
        else:
            revisions = ["I checked the packet and corrected this answer."]
            source = case.context
        for revised in revisions:
            run.results[1].output = revised
            final_prompt = render_prompt(recipe.steps[2].prompt, run)
            if revised not in final_prompt or source not in final_prompt:
                raise RuntimeError(f"{case.title} did not carry its inputs forward.")


def verify_portable_chain():
    answers = iter(("A dictionary maps keys to values.", "Try reading one key from a settings dictionary."))

    def fixture_model(_model, _prompt):
        return next(answers), None

    outputs, prompts = MinimalChainable.run(
        context={"topic": "Python dictionaries"},
        model="offline fixture",
        llm_callable=fixture_model,
        prompts=["Explain {{topic}} briefly.", "Use this explanation in one exercise:\n{{output[-1]}}"],
    )
    if len(outputs) != 2 or outputs[0] not in prompts[1]:
        raise RuntimeError("The portable chain fixture did not complete its handoff.")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args(argv)
    verify_workbench_examples()
    verify_portable_chain()
    print(f"Offline examples passed: Moon walkthrough, {len(PRACTICE_CASES)} practice cases, portable chain.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
