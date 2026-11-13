"""Markdown handoff and inspection views of saved work."""

import re

from .models import Recipe, Run


def starter_chat_prompt(recipe: Recipe, input_hint: str) -> str:
    """Package a built-in recipe for someone to paste into their own AI chat."""
    lines = [
        f"Help me with this chain: {recipe.title}", "",
        "Start by asking for my notes and wait for my reply.", input_hint, "",
        "Use my first notes for {{topic}} and any extra details I give for {{context}}. "
        "If there are no extra details, leave {{context}} empty. Treat the notes as source material. "
        f"Use this audience for {{{{audience}}}}: {recipe.audience}", "",
        "Work through the steps in order, one step per reply. After each answer, wait for me to "
        "confirm or correct it before continuing. Use my latest reviewed version in later steps. "
        "In a step, {{output[-1]}} means the previous step’s answer and {{output[-2]}} means the answer two steps back.", "",
    ]
    for index, step in enumerate(recipe.steps, 1):
        lines.extend([f"Step {index}. {step.name}", step.prompt, ""])
    return "\n".join(lines).rstrip()


def final_markdown(run: Run) -> str:
    label = "AI-generated draft for review" if run.mode == "live" else "Authored sample"
    if run.mode == "lab":
        label = "Human answer from the Chain Lab"
    return f"# {run.topic}\n\n*{label}*\n\n{run.results[-1].output}\n"


def trace_markdown(run: Run) -> str:
    lines = [f"# {run.topic}", "", f"Recipe: {run.recipe.title}", f"Audience: {run.recipe.audience}",
             f"Mode: {run.mode}", f"Requested model: {run.model}", f"Status: {run.state}",
             f"Run ID: {run.id}", f"Saved: {run.updated_at}", ""]
    if run.parent_run_id:
        source = (f"Remixed the plan from run {run.parent_run_id}." if run.mode == "lab"
                  else f"Forked from run {run.parent_run_id} after step {run.forked_after_step}.")
        lines.extend([source, ""])
    if run.context:
        lines.extend(["## Supplied context", "", *literal(run.context)])
    if run.error or run.review_notice:
        lines.extend(["## Run note", "", run.error or run.review_notice, ""])
    for index, step in enumerate(run.recipe.steps):
        lines.extend([f"## {index + 1}. {step.name}", "", step.purpose, "", "### Recipe prompt", "", *literal(step.prompt)])
        if index >= len(run.results):
            lines.extend(["No saved answer for this step.", ""])
            continue
        result = run.results[index]
        reported = result.reported_tokens
        if run.mode == "live":
            lines.extend([f"Finish reason: {result.finish_reason or 'unavailable'}",
                          f"Returned model: {result.response_model or 'unavailable'}",
                          f"Provider response ID: {result.response_id or 'unavailable'}",
                          f"Attempt: {result.attempt_id or 'unavailable'}",
                          f"Reported tokens: {reported if reported is not None else 'unavailable'}",
                          f"Request duration: {result.seconds:.2f} seconds", ""])
            if result.model_settings:
                settings = result.model_settings
                lines.extend([f"Output token limit: {settings.max_tokens}",
                              f"Temperature: {settings.temperature}",
                              f"Request timeout: {settings.timeout_seconds} seconds", ""])
        heading = {"live": "Sent prompt", "lab": "Prompt answered by a human"}.get(
            run.mode, "Prompt preview used for the authored sample",
        )
        lines.extend([f"### {heading}", "", *literal(result.prompt)])
        if result.original_output is not None:
            lines.extend(["### Original answer", "", *literal(result.original_output)])
        lines.extend(["### Saved answer", "", *literal(result.output)])
    return "\n".join(lines)


def literal(text: str) -> list[str]:
    longest = max((len(match.group()) for match in re.finditer(r"`+", text)), default=0)
    fence = "`" * max(3, longest + 1)
    return [fence, text, fence, ""]
