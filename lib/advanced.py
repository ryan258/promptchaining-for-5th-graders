"""Portable Advanced operations. HTML/API routes supply inputs and offload calls."""

import json
from pathlib import Path
import subprocess
import sys

from .core.chain import MinimalChainable
from .core.errors import InputError
from .core.limits import bounded_count, validate_prompts
from .core.llm_client import prompt
from .core.meta_chain_generator import MetaChainGenerator


def planned_requests(name: str, payload: dict) -> int:
    """Maximum logical calls for a validated built-in pattern; no auto retries."""
    if name in {"socratic_dialogue", "adversarial_socratic"}:
        return 2 * bounded_count(payload["depth"], "depth") + 2
    if name == "red_vs_blue":
        return 2 * bounded_count(payload["rounds"], "rounds") + 2
    if name == "five_whys":
        return bounded_count(payload["depth"], "depth") + 2
    return {"scientific_method": 5, "design_thinking": 5,
            "judicial_reasoning": 5, "dialectical": 4}[name]


def normalize_payload(registry: dict, name: str, payload: dict) -> dict:
    entry = registry.get(name)
    if entry is None:
        raise InputError("Choose an installed reasoning pattern.", 404)
    if not isinstance(payload, dict):
        raise InputError("Pattern inputs must be an object.")
    result = {}
    for field, spec in entry.get("input_schema", {}).items():
        value = next((payload[key] for key in [field, *spec.get("aliases", [])]
                      if key in payload and payload[key] not in (None, "")), None)
        if value is None:
            if spec.get("required"):
                raise InputError(f"{field} is required for {name}.")
            value = spec.get("default")
        if spec.get("required") and isinstance(value, str) and not value.strip():
            raise InputError(f"{field} is required for {name}.")
        coerce = spec.get("coerce")
        if value is not None:
            try:
                if coerce == "string_list":
                    value = [item.strip() for item in value.replace(",", "\n").splitlines() if item.strip()] if isinstance(value, str) else value
                    if not isinstance(value, list) or len(value) > 30 or any(not isinstance(v, str) or len(v) > 16000 for v in value):
                        raise ValueError()
                elif coerce is bool:
                    if isinstance(value, str) and value.lower() in {"true", "false", "yes", "no", "1", "0", "on", "off"}:
                        value = value.lower() in {"true", "yes", "1", "on"}
                    elif not isinstance(value, bool):
                        raise ValueError()
                elif coerce is int:
                    if isinstance(value, bool) or isinstance(value, float):
                        raise ValueError()
                    value = int(value)
                elif coerce:
                    value = coerce(value)
                elif not isinstance(value, str) or len(value) > 16000:
                    raise ValueError()
            except (TypeError, ValueError):
                raise InputError(f"Invalid value for {field} in {name}.") from None
        if field in {"depth", "rounds"}:
            bounded_count(value, field)
        result[field] = value
    return result


def execute_pattern(registry: dict, name: str, payload: dict) -> dict:
    kwargs = normalize_payload(registry, name, payload)
    result, metadata = registry[name]["function"](**kwargs)
    return {"status": "success", "pattern": name, "result": result, "metadata": metadata}


def design_chain(goal: str, context: dict, constraints: list, generator_factory=MetaChainGenerator) -> dict:
    if not isinstance(goal, str) or not goal.strip() or len(goal) > 500:
        raise InputError("Give the design a goal of 1–500 characters.")
    if not isinstance(context, dict) or len(context) > 20 or len(json.dumps(context)) > 16000:
        raise InputError("Keep design context within 20 fields and 16,000 characters.")
    if not isinstance(constraints, list) or len(constraints) > 30 or any(not isinstance(c, str) or len(c) > 1000 for c in constraints):
        raise InputError("Use at most 30 short design constraints.")
    generator = generator_factory()
    return generator.design_chain(goal, context, constraints).to_dict()


def execute_design(data: dict, generator_factory=MetaChainGenerator, llm_callable=prompt) -> dict:
    if not isinstance(data, dict) or not data.get("prompts"):
        raise InputError("Design must include prompts to execute")
    validate_prompts(data["prompts"], maximum=8)
    context = data.get("context") or {}
    if not isinstance(context, dict) or len(json.dumps(context)) > 16000:
        raise InputError("Keep design context within 16,000 characters.")
    goal = data.get("goal", "meta_chain_run")
    if not isinstance(goal, str) or len(goal) > 500:
        raise InputError("Keep the design goal within 500 characters.")
    generator = generator_factory()
    outputs, sent, usage, trace = MinimalChainable.run(
        context=context, model=generator.model_info, llm_callable=llm_callable,
        prompts=data["prompts"], return_trace=True, artifact_store=generator.artifact_store,
        topic=goal.lower().replace(" ", "_")[:50],
    )
    trace["final_result"] = outputs[-1] if outputs else None
    return {"status": "success", "execution_trace": trace, "outputs": outputs, "prompts": sent, "usage": usage}


def execute_tool(path: str, root: str, category: str, name: str, topic: str, context: str = "") -> dict:
    if not topic.strip() or len(topic) > 3000 or len(context) > 16000:
        raise InputError("Give the tool a topic of 1–3,000 characters and context up to 16,000 characters.")
    command = [sys.executable, path, topic]
    if context:
        command.extend(["--context", context])
    result = subprocess.run(command, cwd=root, capture_output=True, text=True, timeout=300)
    if result.returncode:
        raise InputError("The tool could not finish. Check setup and provider usage before trying again.", 502)
    # Prefer the structured result over the later log marker. Never read an
    # arbitrary path mentioned in model text or return raw subprocess diagnostics.
    for marker, kind in (("✅ Saved JSON to:", "json"), ("✅ Log saved to:", "markdown")):
        for line in result.stdout.splitlines():
            if not line.startswith(marker):
                continue
            candidate = Path(line[len(marker):].strip())
            candidate = (Path(root) / candidate).resolve()
            if not any(candidate.is_relative_to((Path(root) / folder).resolve()) for folder in ("output", "logs")):
                continue
            if not candidate.is_file() or candidate.stat().st_size > 10_000_000:
                continue
            content = candidate.read_text(encoding="utf-8")
            return {"status": "success", "tool_name": name, "category": category,
                    "output": json.loads(content) if kind == "json" else content,
                    "type": kind, "logs": "Completed. Full private traces remain in the local logs folder."}
    raise InputError("The tool finished without a readable saved result. Check the local output folder.", 502)
