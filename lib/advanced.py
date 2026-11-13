"""Portable Advanced operations. HTML/API routes supply inputs and offload calls."""

import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from uuid import uuid4

from .core.chain import MinimalChainable
from .core.errors import InputError
from .core.limits import bounded_count, validate_prompts
from .core.llm_client import request_completion
from .core.meta_chain_generator import MetaChainGenerator
from .core.templates import validate_template_inputs


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


def prepare_comparison(registry: dict, topic: str, chain_name: str = "scientific_method",
                       chain_kwargs: dict | None = None, baseline_prompt: str | None = None) -> dict:
    """Validate the entire comparison before any model or artifact work."""
    if not isinstance(topic, str) or not topic.strip() or len(topic) > 16000:
        raise InputError("Give the comparison a topic of 1–16,000 characters.")
    if not isinstance(chain_name, str):
        raise InputError("Choose an installed reasoning pattern for comparison.")
    pattern = registry.get(chain_name)
    if not pattern or not pattern.get("supports_emergence"):
        raise InputError("Choose a reasoning pattern that supports comparison.", 404)
    if baseline_prompt is not None and (not isinstance(baseline_prompt, str)
                                        or not baseline_prompt.strip() or len(baseline_prompt) > 16000):
        raise InputError("Give the custom baseline 1–16,000 characters.")
    if chain_kwargs is None:
        chain_kwargs = {}
    if not isinstance(chain_kwargs, dict):
        raise InputError("Comparison pattern inputs must be an object.")
    schema = pattern["input_schema"]
    fields = {key for field, spec in schema.items() for key in (field, *spec.get("aliases", []))}
    if chain_kwargs.keys() - fields:
        raise InputError("Remove unrecognized comparison pattern inputs.")
    for field, spec in schema.items():
        if "topic" in spec.get("aliases", ()):
            for key in ("topic", field):
                if key in chain_kwargs and chain_kwargs[key] != topic:
                    raise InputError("Use the same topic for the chain, baseline and assessment.")
    inputs = normalize_payload(registry, chain_name, {**chain_kwargs, "topic": topic})
    return {"topic": topic, "chain_function": pattern["function"], "chain_name": chain_name,
            "baseline_prompt": baseline_prompt, **inputs}


def design_chain(goal: str, context: dict, constraints: list, generator_factory=MetaChainGenerator) -> dict:
    if not isinstance(goal, str) or not goal.strip() or len(goal) > 500:
        raise InputError("Give the design a goal of 1–500 characters.")
    if not isinstance(context, dict) or len(context) > 20 or len(json.dumps(context)) > 16000:
        raise InputError("Keep design context within 20 fields and 16,000 characters.")
    if not isinstance(constraints, list) or len(constraints) > 30 or any(not isinstance(c, str) or len(c) > 1000 for c in constraints):
        raise InputError("Use at most 30 short design constraints.")
    generator = generator_factory()
    design = generator.design_chain(goal, context, constraints).to_dict()
    _validated_design_inputs(design)
    return design


def _validated_design_inputs(data: dict) -> tuple[list[str], dict, str]:
    if not isinstance(data, dict) or not data.get("prompts"):
        raise InputError("Design must include prompts to execute")
    validate_prompts(data["prompts"], maximum=8)
    context = data.get("context", {})
    if not isinstance(context, dict) or len(json.dumps(context)) > 16000:
        raise InputError("Keep design context within 16,000 characters.")
    goal = data.get("goal", "meta_chain_run")
    if not isinstance(goal, str) or len(goal) > 500:
        raise InputError("Keep the design goal within 500 characters.")
    validate_template_inputs(data["prompts"], context, allow_artifacts=False)
    return data["prompts"], context, goal


def execute_design(data: dict, generator_factory=MetaChainGenerator, llm_callable=request_completion) -> dict:
    prompts, context, goal = _validated_design_inputs(data)
    generator = generator_factory()
    outputs, sent, usage, trace = MinimalChainable.run(
        context=context, model=generator.model_info, llm_callable=llm_callable,
        prompts=prompts, return_trace=True, artifact_store=generator.artifact_store,
        topic=f"{goal[:50]}_run_{uuid4().hex[:12]}",
    )
    trace["final_result"] = outputs[-1] if outputs else None
    return {"status": "success", "partial": trace.get("completion_complete") is False,
            "execution_trace": trace, "outputs": outputs, "prompts": sent, "usage": usage}


def execute_tool(path: str, root: str, category: str, name: str, topic: str, context: str = "") -> dict:
    if not topic.strip() or len(topic) > 3000 or len(context) > 16000:
        raise InputError("Give the tool a topic of 1–3,000 characters and context up to 16,000 characters.")
    if name == "subject_connector" and not context.strip():
        raise InputError("Enter both subjects before running Subject Connector.")
    with TemporaryDirectory(prefix="studio-tool-") as directory:
        result_path = Path(directory) / "result.json"
        command = [sys.executable, path, "--result-file", str(result_path)]
        result = subprocess.run(command, cwd=root, input=json.dumps({"topic": topic, "context": context}),
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, text=True, timeout=300)
        if result.returncode:
            raise InputError("The tool could not finish. Check setup and provider usage before trying again.", 502)
        try:
            if result_path.is_symlink() or not result_path.is_file() or result_path.stat().st_size > 10_000_000:
                raise ValueError()
            output = json.loads(result_path.read_text(encoding="utf-8"))
            if not isinstance(output, dict):
                raise ValueError()
        except (OSError, ValueError, RecursionError):
            raise InputError("The tool finished without a readable saved result. Check the local output folder.", 502) from None
    return {"status": "success", "tool_name": name, "category": category, "output": output,
            "partial": output.get("completion_complete") is False, "type": "json",
            "logs": "The private trace remains in the local logs folder."}
