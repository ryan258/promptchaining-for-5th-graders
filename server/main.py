import ast
import os
import sys
import glob
import subprocess
import json
import logging
from dataclasses import dataclass
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from collections.abc import Mapping
from contextlib import asynccontextmanager
from urllib.parse import urlsplit
from fastapi import FastAPI, HTTPException, Body, Request, Form
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.concurrency import run_in_threadpool
from starlette.middleware.trustedhost import TrustedHostMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from lib.core.meta_chain_generator import MetaChainGenerator
from lib.core.chain import MinimalChainable
from lib.core.llm_client import prompt as core_prompt
from lib.enhancements.natural_reasoning import REASONING_PATTERNS
from lib.enhancements.adversarial_chains import ADVERSARIAL_PATTERNS
from lib.enhancements.emergence_measurement import measure_emergence
from lib.utils.demo_examples import (
    get_adversarial_demo_examples,
    get_meta_demo_examples,
    get_reasoning_demo_examples,
    get_tool_demo_examples,
)
from server import workbench, guides
from lib import advanced
from lib.core.errors import InputError, user_error

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(_app):
    workbench.get_runner()
    try:
        yield
    finally:
        await run_in_threadpool(workbench.close_workbench)


app = FastAPI(title="Prompt Chaining Studio", lifespan=lifespan)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1", "[::1]", "testserver"])


@app.middleware("http")
async def local_request_boundary(request: Request, call_next):
    if request.method not in {"GET", "HEAD", "OPTIONS"}:
        origin = request.headers.get("origin")
        if origin:
            try:
                parsed = urlsplit(origin)
                same_origin = (parsed.scheme, parsed.netloc.lower()) == (request.url.scheme, request.url.netloc.lower())
            except ValueError:
                same_origin = False
            if not same_origin:
                return PlainTextResponse("Open this action from your local Studio tab.", status_code=403)
        if request.headers.get("sec-fetch-site") == "cross-site":
            return PlainTextResponse("Open this action from your local Studio tab.", status_code=403)
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    if not request.url.path.startswith("/static/"):
        response.headers["Cache-Control"] = "no-store"
    return response

TEMPLATES_DIR = os.path.join(PROJECT_ROOT, "server", "templates")
STATIC_DIR = os.path.join(PROJECT_ROOT, "server", "static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)
app.state.templates = templates
templates.env.filters["local_date"] = workbench.local_date
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.include_router(workbench.router)
app.include_router(guides.router)

def _pretty_json(data: Any) -> str:
    if isinstance(data, str):
        return data
    try:
        return json.dumps(data, indent=2, ensure_ascii=False)
    except TypeError:
        return str(data)

def _humanize_key(value: Any) -> str:
    text = str(value or "").replace("_", " ").replace("-", " ").strip()
    return text.title() if text else ""

def _format_timestamp(value: Any) -> str:
    try:
        return datetime.fromtimestamp(float(value)).strftime("%b %d, %Y at %I:%M %p")
    except (TypeError, ValueError, OSError):
        return str(value)

def _format_bytes(value: Any) -> str:
    try:
        size = float(value)
    except (TypeError, ValueError):
        return str(value)
    units = ["B", "KB", "MB", "GB"]
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.0f} {unit}" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} GB"

def _preview_text(value: Any, limit: int = 180) -> str:
    if isinstance(value, (dict, list)):
        text = _pretty_json(value)
    else:
        text = str(value or "")
    condensed = " ".join(text.split())
    return condensed if len(condensed) <= limit else condensed[: limit - 1].rstrip() + "..."

templates.env.filters["pretty_json"] = _pretty_json
templates.env.filters["humanize"] = _humanize_key
templates.env.filters["format_timestamp"] = _format_timestamp
templates.env.filters["format_bytes"] = _format_bytes
templates.env.filters["preview_text"] = _preview_text

TOOLS_DIR = os.path.join(PROJECT_ROOT, 'tools')
ARTIFACTS_DIR = os.path.join(PROJECT_ROOT, 'artifacts')
ARTIFACTS_ROOT = Path(ARTIFACTS_DIR).resolve()
INTERNAL_ARTIFACT_TOPICS = {"_chroma"}

# Only expose tools that match the expected CLI contract:
#   python3 <tool_path> <topic> [--context <text>]
ALLOWED_TOOLS = {
    ("learning", "concept_simplifier"),
    ("learning", "subject_connector"),
}

class Tool(BaseModel):
    name: str
    category: str
    description: str


class ArtifactSummary(BaseModel):
    topic: str
    filename: str
    size: int
    modified: float


@dataclass(frozen=True)
class _ToolRecord:
    name: str
    category: str
    path: str
    description: str


class RunRequest(BaseModel):
    tool_name: str
    category: str
    topic: str
    context: Optional[str] = ""


class MetaDesignRequest(BaseModel):
    goal: str = Field(..., min_length=1, max_length=500)
    context: Dict[str, Any] = Field(default_factory=dict, max_length=20)
    constraints: List[str] = Field(default_factory=list, max_length=30)


class MetaExecuteRequest(BaseModel):
    design: Dict[str, Any]

STUDIO_NAV = (
    ("home", "Workbench", "/"),
    ("recipes", "Recipes", "/studio/recipes"),
    ("library", "My library", "/studio/library"),
    ("learn", "Guides", "/studio/guides"),
    ("advanced", "Advanced", "/studio/advanced"),
)

TEXTAREA_FIELDS = {
    "topic",
    "context",
    "hypothesis",
    "belief",
    "problem",
    "case",
    "thesis",
    "claim",
    "position_to_defend",
}

FIELD_HELP_TEXT = {
    "hypothesis": "State the idea you want to test.",
    "belief": "Write the belief or assumption you want examined.",
    "problem": "Describe the problem in plain language.",
    "case": "Describe the dilemma, case, or decision to weigh.",
    "topic": "Name the topic or domain for the run.",
    "context": "Optional background, audience notes, or constraints.",
    "evidence_sources": "Optional. Enter one source per line.",
    "teacher_persona": "Who should guide the questioning?",
    "depth": "How many rounds of questioning to run.",
    "target_user": "Who are you designing for?",
    "constraints": "Optional. Enter one constraint per line.",
    "relevant_principles": "Optional. Enter one principle per line.",
    "precedents": "Optional. Enter one precedent per line.",
    "position_to_defend": "Write the exact claim Blue Team should defend.",
    "rounds": "How many attack and defense rounds to run.",
    "judge_criteria": "Optional. Enter one judging criterion per line.",
    "thesis": "State the thesis or claim to challenge.",
    "domain": "Optional area or context for the debate.",
    "claim": "Write the claim you want stress-tested.",
    "aggressive": "Choose how confrontational the questioning should be.",
}

FIELD_PLACEHOLDERS = {
    "hypothesis": "Students learn fractions faster with sports analogies",
    "belief": "Homework should be optional",
    "problem": "Students forget to bring their reading logs",
    "case": "Should recess be longer for elementary students?",
    "topic": "Photosynthesis",
    "context": "Audience: 5th graders\nTone: concrete and vivid",
    "evidence_sources": "Science textbook\nClassroom observation\nLab notes",
    "teacher_persona": "Curious science teacher",
    "target_user": "5th grade student",
    "constraints": "Keep it visual\nUse familiar examples",
    "relevant_principles": "Fairness\nStudent safety\nLong-term learning",
    "precedents": "Other districts increased recess time",
    "position_to_defend": "School lunch should be free for all students",
    "judge_criteria": "Logic\nEvidence\nPractical trade-offs",
    "thesis": "Students should use calculators earlier in math class",
    "domain": "Elementary math education",
    "claim": "AI tutors can improve reading comprehension",
}





def _split_text_lines(value: Any) -> Optional[List[str]]:
    if value in (None, ""):
        return None
    if isinstance(value, list):
        items = [str(item).strip() for item in value if str(item).strip()]
        return items or None

    items = []
    for raw_line in str(value).replace(",", "\n").splitlines():
        item = raw_line.strip()
        if item:
            items.append(item)
    return items or None


def _parse_context_text(raw_text: str) -> Dict[str, Any]:
    text = (raw_text or "").strip()
    if not text:
        return {}

    context: Dict[str, Any] = {}
    loose_notes: List[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            normalized_key = key.strip().lower().replace(" ", "_")
            normalized_value = value.strip()
            if normalized_key and normalized_value:
                context[normalized_key] = normalized_value
                continue
        loose_notes.append(line)

    if loose_notes:
        context["notes"] = "\n".join(loose_notes) if context else text

    return context or {"notes": text}




def _normalize_registry_payload(
    registry: Dict[str, Dict[str, Any]],
    pattern_name: str,
    payload: Dict[str, Any],
) -> Dict[str, Any]:
    try:
        return advanced.normalize_payload(registry, pattern_name, payload)
    except InputError as exc:
        raise HTTPException(status_code=exc.status, detail=str(exc)) from None


def _extract_module_description(source: str) -> str:
    try:
        module = ast.parse(source)
    except SyntaxError:
        return "No description available."

    docstring = ast.get_docstring(module, clean=True)
    if not docstring:
        return "No description available."

    lines = [line.strip() for line in docstring.splitlines() if line.strip()]
    if len(lines) >= 2:
        return lines[1]
    if lines:
        return lines[0]
    return "No description available."


def _navigation(active_page: str) -> List[Dict[str, Any]]:
    return [
        {
            "slug": slug,
            "label": label,
            "href": href,
            "active": slug == active_page or (slug == "advanced" and active_page in {"tools", "reasoning", "adversarial", "meta", "artifacts"}),
        }
        for slug, label, href in STUDIO_NAV
    ]


def _page_context(active_page: str, title: str, **extra: Any) -> Dict[str, Any]:
    context = {
        "title": title,
        "nav_items": _navigation(active_page),
        "active_page": active_page,
    }
    context.update(extra)
    return context


def _field_input_kind(field_name: str, spec: Dict[str, Any]) -> str:
    coerce = spec.get("coerce")
    if coerce == "string_list":
        return "textarea"
    if coerce is int:
        return "number"
    if coerce is bool:
        return "select"
    if field_name in TEXTAREA_FIELDS:
        return "textarea"
    return "text"


def _field_default_value(spec: Dict[str, Any]) -> str:
    default = spec.get("default")
    if default is None:
        return ""
    if isinstance(default, bool):
        return "true" if default else "false"
    return str(default)


def _build_field_view(field_name: str, spec: Dict[str, Any]) -> Dict[str, Any]:
    kind = _field_input_kind(field_name, spec)
    return {
        "name": field_name,
        "label": _humanize_key(field_name),
        "kind": kind,
        "required": bool(spec.get("required")),
        "help_text": FIELD_HELP_TEXT.get(field_name, "Optional input for this pattern."),
        "placeholder": FIELD_PLACEHOLDERS.get(field_name, f"Enter {_humanize_key(field_name).lower()}"),
        "default_value": _field_default_value(spec),
        "minimum": 1 if field_name in {"depth", "rounds"} else None,
        "maximum": 5 if field_name in {"depth", "rounds"} else None,
        "full_width": kind == "textarea",
        "rows": 6 if kind == "textarea" else None,
        "options": [
            {"label": "Yes", "value": "true"},
            {"label": "No", "value": "false"},
        ] if kind == "select" else [],
    }


def _build_pattern_view(registry: Mapping[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    patterns: List[Dict[str, Any]] = []
    for name, info in registry.items():
        schema = info.get("input_schema") or {}
        patterns.append(
            {
                "name": name,
                "display_name": _humanize_key(name),
                "description": info.get("description", ""),
                "use_when": info.get("use_when", ""),
                "example": info.get("example", ""),
                "request_field": "rounds" if name == "red_vs_blue" else "depth" if "depth" in schema else "",
                "request_factor": 1 if name == "five_whys" else 2,
                "request_base": 2,
                "request_count": advanced.planned_requests(name, {key: spec.get("default") for key, spec in schema.items()}),
                "fields": [
                    _build_field_view(field_name, spec)
                    for field_name, spec in schema.items()
                ],
            }
        )
    return patterns


def _collect_form_payload(
    form_data: Mapping[str, Any],
    registry: Dict[str, Dict[str, Any]],
    pattern_name: str,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {}
    schema = (registry.get(pattern_name) or {}).get("input_schema") or {}

    payload_json = str(form_data.get("payload_json", "") or "").strip()
    if payload_json:
        payload.update(_parse_json_payload(payload_json))

    for field_name, spec in schema.items():
        raw_value = form_data.get(field_name)
        if raw_value in (None, ""):
            continue
        if spec.get("coerce") == "string_list":
            payload[field_name] = _split_text_lines(raw_value)
        else:
            payload[field_name] = raw_value

    topic = form_data.get("topic")
    if topic not in (None, "") and "topic" not in payload:
        payload["topic"] = topic

    return payload


@lru_cache(maxsize=1)
def _scan_tools() -> tuple[_ToolRecord, ...]:
    """Scan the tools directory and return available tools."""
    tools: List[_ToolRecord] = []
    pattern = os.path.join(TOOLS_DIR, "*", "*.py")
    for file_path in glob.glob(pattern):
        if "__init__" in file_path:
            continue

        category = os.path.basename(os.path.dirname(file_path))
        filename = os.path.basename(file_path)
        name = filename.replace(".py", "")

        if (category, name) not in ALLOWED_TOOLS:
            continue

        description = "No description available."
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                description = _extract_module_description(f.read())
        except (IOError, UnicodeDecodeError):
            pass

        tools.append(_ToolRecord(
            name=name,
            category=category,
            path=file_path,
            description=description
        ))

    tools.sort(key=lambda x: (x.category, x.name))
    return tuple(tools)


def _public_tools() -> List[Tool]:
    return [
        Tool(name=tool.name, category=tool.category, description=tool.description)
        for tool in _scan_tools()
    ]


def _resolve_tool_path(category: str, tool_name: str) -> Optional[str]:
    """Return a verified tool path for known tools."""
    for tool in _scan_tools():
        if tool.category == category and tool.name == tool_name:
            return tool.path
    return None


def _is_public_artifact_topic(topic: str) -> bool:
    return bool(topic) and not topic.startswith(".") and topic not in INTERNAL_ARTIFACT_TOPICS


def _is_public_artifact_filename(filename: str) -> bool:
    return bool(filename) and not filename.startswith(".") and not filename.endswith(".meta.json")


def _safe_artifact_path(topic: str, filename: str) -> Path:
    """Resolve artifact path and enforce containment within artifacts root."""
    if not _is_public_artifact_topic(topic) or not _is_public_artifact_filename(filename):
        raise HTTPException(status_code=400, detail="Invalid artifact path")
    candidate = (ARTIFACTS_ROOT / topic / filename).resolve()
    try:
        candidate.relative_to(ARTIFACTS_ROOT)
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid artifact path") from e
    return candidate


def _safe_message(exc: Exception) -> str:
    logger.warning("Advanced operation stopped (%s)", type(exc).__name__)
    if isinstance(exc, HTTPException):
        return str(exc.detail)
    if isinstance(exc, subprocess.TimeoutExpired):
        return "The tool timed out and may have sent requests. Check provider usage before trying again."
    return user_error(exc)


def _api_error(exc: Exception) -> HTTPException:
    if isinstance(exc, HTTPException):
        return exc
    status = exc.status if isinstance(exc, InputError) else 504 if isinstance(exc, subprocess.TimeoutExpired) else 500
    return HTTPException(status_code=status, detail=_safe_message(exc))


@app.get("/tools", response_model=List[Tool])
async def list_tools():
    """Scan the tools directory and return available tools."""
    return _public_tools()

def _execute_tool(category: str, tool_name: str, topic: str, context: Optional[str] = "") -> Dict[str, Any]:
    tool_path = _resolve_tool_path(category, tool_name)
    if tool_path is None:
        raise HTTPException(status_code=404, detail="Tool not found")
    return advanced.execute_tool(tool_path, PROJECT_ROOT, category, tool_name, topic, context or "")

@app.post("/run")
async def run_tool(request: RunRequest):
    try:
        return await run_in_threadpool(_execute_tool, request.category, request.tool_name, request.topic, request.context)
    except Exception as exc:
        raise _api_error(exc) from None


@app.get("/patterns")
async def list_reasoning_patterns():
    """List available reasoning patterns with descriptions."""
    patterns = []
    for name, info in REASONING_PATTERNS.items():
        patterns.append({
            "name": name,
            "description": info.get("description", ""),
            "use_when": info.get("use_when", ""),
            "example": info.get("example", "")
        })
    return patterns

def _execute_pattern(pattern_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    return advanced.execute_pattern(REASONING_PATTERNS, pattern_name, payload)

@app.post("/patterns/{pattern_name}")
async def run_pattern(pattern_name: str, payload: Dict[str, Any] = Body(...)):
    try:
        return await run_in_threadpool(_execute_pattern, pattern_name, payload or {})
    except Exception as exc:
        raise _api_error(exc) from None


@app.get("/adversarial")
async def list_adversarial_patterns():
    """List available adversarial reasoning patterns."""
    patterns = []
    for name, info in ADVERSARIAL_PATTERNS.items():
        patterns.append({
            "name": name,
            "description": info.get("description", ""),
            "use_when": info.get("use_when", ""),
            "example": info.get("example", "")
        })
    return patterns

def _execute_adversarial(pattern_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    return advanced.execute_pattern(ADVERSARIAL_PATTERNS, pattern_name, payload)

@app.post("/adversarial/{pattern_name}")
async def run_adversarial(pattern_name: str, payload: Dict[str, Any] = Body(...)):
    try:
        return await run_in_threadpool(_execute_adversarial, pattern_name, payload or {})
    except Exception as exc:
        raise _api_error(exc) from None


def _execute_meta_chain_design(design_data: Dict[str, Any]) -> Dict[str, Any]:
    return advanced.execute_design(design_data, generator_factory=MetaChainGenerator, llm_callable=core_prompt)


@app.post("/meta-chain/design")
async def design_meta_chain(request: MetaDesignRequest):
    try:
        design = await run_in_threadpool(advanced.design_chain, request.goal, request.context,
                                        request.constraints, generator_factory=MetaChainGenerator)
        return {"status": "success", "design": design}
    except Exception as exc:
        raise _api_error(exc) from None


@app.post("/meta-chain/execute")
async def execute_meta_chain(request: MetaExecuteRequest):
    try:
        return await run_in_threadpool(_execute_meta_chain_design, request.design or {})
    except Exception as exc:
        raise _api_error(exc) from None


@app.post("/emergence/compare")
async def compare_emergence(payload: Dict[str, Any] = Body(...)):
    """Compare chain vs baseline outputs to measure emergence."""
    topic = payload.get("topic")
    if not topic:
        raise HTTPException(status_code=400, detail="topic is required for emergence comparison")

    chain_name = payload.get("chain_name", "scientific_method")
    chain_kwargs = payload.get("chain_kwargs") or {}
    pattern = REASONING_PATTERNS.get(chain_name)
    if not pattern or not pattern.get("supports_emergence"):
        raise HTTPException(
            status_code=404,
            detail=f"Chain '{chain_name}' not supported for emergence. Available: {', '.join(name for name, info in REASONING_PATTERNS.items() if info.get('supports_emergence'))}"
        )

    baseline_prompt = payload.get("baseline_prompt")
    normalized_kwargs = _normalize_registry_payload(
        REASONING_PATTERNS,
        chain_name,
        {"topic": topic, **chain_kwargs},
    )

    try:
        comparison, metadata = await run_in_threadpool(measure_emergence,
            topic=topic,
            chain_function=pattern["function"],
            baseline_prompt=baseline_prompt,
            chain_name=chain_name,
            **normalized_kwargs,
        )
    except Exception as e:
        raise _api_error(e) from None

    return {
        "status": "error" if comparison.get("status") == "failed" else "success",
        "comparison": comparison,
        "metadata": metadata
    }

@app.get("/artifacts", response_model=List[ArtifactSummary])
async def list_artifacts():
    """List all artifacts in the artifacts directory."""
    if not os.path.exists(ARTIFACTS_DIR):
        return []

    artifacts: List[ArtifactSummary] = []
    try:
        for topic in os.listdir(ARTIFACTS_DIR):
            topic_path = os.path.join(ARTIFACTS_DIR, topic)
            if not os.path.isdir(topic_path) or not _is_public_artifact_topic(topic):
                continue

            for filename in os.listdir(topic_path):
                if not _is_public_artifact_filename(filename):
                    continue

                file_path = os.path.join(topic_path, filename)
                if os.path.isfile(file_path):
                    stat = os.stat(file_path)
                    artifacts.append(
                        ArtifactSummary(
                            topic=topic,
                            filename=filename,
                            size=stat.st_size,
                            modified=stat.st_mtime,
                        )
                    )
    except Exception as e:
        logger.error(f"Error listing artifacts: {e}")
        raise HTTPException(status_code=500, detail="Unable to list artifacts") from e

    artifacts.sort(key=lambda x: x.modified, reverse=True)
    return artifacts

@app.get("/artifacts/{topic}/{filename}")
async def get_artifact(topic: str, filename: str):
    """Get the content of a specific artifact."""
    file_path = _safe_artifact_path(topic, filename)

    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="Artifact not found")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Try to parse as JSON
        try:
            content = json.loads(content)
            return {"content": content, "type": "json"}
        except json.JSONDecodeError:
            return {"content": content, "type": "text"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/artifacts/{topic}/{filename}")
async def delete_artifact(topic: str, filename: str):
    """Delete a specific artifact."""
    file_path = _safe_artifact_path(topic, filename)

    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="Artifact not found")

    try:
        file_path.unlink()

        # Remove topic directory if empty
        topic_path = file_path.parent
        if topic_path.is_dir() and not any(topic_path.iterdir()):
            topic_path.rmdir()

        return {"status": "success", "message": "Artifact deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def _group_tools_by_category(tools: List[Tool]) -> Dict[str, List[Tool]]:
    grouped: Dict[str, List[Tool]] = {}
    for tool in tools:
        grouped.setdefault(tool.category, []).append(tool)
    return grouped


@app.get("/studio/tools", response_class=HTMLResponse)
async def ui_tools_page(request: Request):
    tools = _public_tools()
    return templates.TemplateResponse(
        request,
        "studio_tools.html",
        _page_context(
            "tools",
            "Tools | Prompt Chaining Studio",
            tools=tools,
            tools_by_category=_group_tools_by_category(tools),
            selected_tool_key=f"{tools[0].category}:{tools[0].name}" if tools else "",
            demo_examples=get_tool_demo_examples(
                f"{tool.category}:{tool.name}" for tool in tools
            ),
        ),
    )


@app.get("/studio/reasoning", response_class=HTMLResponse)
async def ui_reasoning_page(request: Request):
    patterns = _build_pattern_view(REASONING_PATTERNS)
    return templates.TemplateResponse(
        request,
        "studio_patterns.html",
        _page_context(
            "reasoning",
            "Reasoning | Prompt Chaining Studio",
            module_name="Reasoning Patterns",
            module_eyebrow="Reasoning Studio",
            module_intro="Choose a reasoning pattern, fill in plain-language prompts, and read the output in a full-width canvas built for the selected chain.",
            module_note="These patterns teach structured thinking. The form adapts to the selected method instead of dumping every possible field on screen.",
            form_action="/ui/run-pattern",
            result_id="pattern-result",
            loading_id="pattern-loading",
            loading_text="Running reasoning chain...",
            result_title="Reasoning output appears here",
            result_body="Pick a pattern, fill its fields, and the run will render below with readable sections and metadata.",
            patterns=patterns,
            demo_examples=get_reasoning_demo_examples(),
        ),
    )


@app.get("/studio/adversarial", response_class=HTMLResponse)
async def ui_adversarial_page(request: Request):
    patterns = _build_pattern_view(ADVERSARIAL_PATTERNS)
    return templates.TemplateResponse(
        request,
        "studio_patterns.html",
        _page_context(
            "adversarial",
            "Adversarial | Prompt Chaining Studio",
            module_name="Adversarial Patterns",
            module_eyebrow="Debate Studio",
            module_intro="Pressure-test claims with debate, dialectic, and aggressive questioning in a workspace dedicated to adversarial reasoning.",
            module_note="The page only shows the inputs for the active adversarial pattern, then gives the result room to breathe.",
            form_action="/ui/run-adversarial",
            result_id="adversarial-result",
            loading_id="adversarial-loading",
            loading_text="Running adversarial chain...",
            result_title="Adversarial output appears here",
            result_body="Expect debate rounds, judgments, and verdicts to land in a much wider result stage.",
            patterns=patterns,
            demo_examples=get_adversarial_demo_examples(),
        ),
    )


@app.get("/studio/meta", response_class=HTMLResponse)
async def ui_meta_page(request: Request):
    return templates.TemplateResponse(
        request,
        "studio_meta.html",
        _page_context(
            "meta",
            "Meta-Chain | Prompt Chaining Studio",
            demo_examples=get_meta_demo_examples(),
        ),
    )


@app.get("/studio/artifacts", response_class=HTMLResponse)
async def ui_artifacts_page(request: Request):
    try:
        artifacts = await list_artifacts()
    except HTTPException:
        artifacts = []

    return templates.TemplateResponse(
        request,
        "studio_artifacts.html",
        _page_context(
            "artifacts",
            "Artifacts | Prompt Chaining Studio",
            artifacts=artifacts,
        ),
    )


@app.post("/ui/run-tool", response_class=HTMLResponse)
async def ui_run_tool(
    request: Request,
    tool_key: str = Form(...),
    topic: str = Form(...),
    context: str = Form(""),
):
    if ":" not in tool_key:
        return templates.TemplateResponse(
            request,
            "partials/error.html",
            {"message": "Invalid tool selection."},
        )

    category, tool_name = tool_key.split(":", 1)

    try:
        result = await run_in_threadpool(_execute_tool, category, tool_name, topic, context)
    except Exception as e:
        return templates.TemplateResponse(
            request,
            "partials/error.html",
            {"message": _safe_message(e)},
        )

    return templates.TemplateResponse(
        request,
        "partials/tool_result.html",
        {"result": result},
    )


def _parse_json_payload(payload_json: str) -> Dict[str, Any]:
    payload_json = (payload_json or "").strip()
    if not payload_json:
        return {}
    return json.loads(payload_json)


@app.post("/ui/run-pattern", response_class=HTMLResponse)
async def ui_run_pattern(
    request: Request,
):
    form = await request.form()
    pattern_name = str(form.get("pattern_name") or "").strip()
    if not pattern_name:
        return templates.TemplateResponse(
            request,
            "partials/error.html",
            {"message": "Select a reasoning pattern before running it."},
        )

    try:
        payload = _collect_form_payload(form, REASONING_PATTERNS, pattern_name)
    except json.JSONDecodeError as e:
        return templates.TemplateResponse(
            request,
            "partials/error.html",
            {"message": "Use a valid JSON object for these inputs."},
        )

    try:
        result = await run_in_threadpool(_execute_pattern, pattern_name, payload)
    except Exception as e:
        return templates.TemplateResponse(
            request,
            "partials/error.html",
            {"message": _safe_message(e)},
        )

    return templates.TemplateResponse(
        request,
        "partials/pattern_result.html",
        {"result": result},
    )


@app.post("/ui/run-adversarial", response_class=HTMLResponse)
async def ui_run_adversarial(
    request: Request,
):
    form = await request.form()
    pattern_name = str(form.get("pattern_name") or "").strip()
    if not pattern_name:
        return templates.TemplateResponse(
            request,
            "partials/error.html",
            {"message": "Select an adversarial pattern before running it."},
        )

    try:
        payload = _collect_form_payload(form, ADVERSARIAL_PATTERNS, pattern_name)
    except json.JSONDecodeError as e:
        return templates.TemplateResponse(
            request,
            "partials/error.html",
            {"message": "Use a valid JSON object for these inputs."},
        )

    try:
        result = await run_in_threadpool(_execute_adversarial, pattern_name, payload)
    except Exception as e:
        return templates.TemplateResponse(
            request,
            "partials/error.html",
            {"message": _safe_message(e)},
        )

    return templates.TemplateResponse(
        request,
        "partials/pattern_result.html",
        {"result": result},
    )


@app.post("/ui/meta-design", response_class=HTMLResponse)
async def ui_meta_design(
    request: Request,
    goal: str = Form(...),
    context_text: str = Form(""),
    context_json: str = Form(""),
    constraints: str = Form(""),
):
    if context_json.strip():
        try:
            context = _parse_json_payload(context_json)
        except json.JSONDecodeError as e:
            return templates.TemplateResponse(
                request,
                "partials/error.html",
                {"message": "Use a valid JSON object for context."},
            )
    else:
        context = _parse_context_text(context_text)

    constraint_list = []
    if constraints:
        for item in constraints.replace(",", "\n").splitlines():
            item = item.strip()
            if item:
                constraint_list.append(item)

    try:
        design = await run_in_threadpool(advanced.design_chain, goal, context, constraint_list,
                                        generator_factory=MetaChainGenerator)
    except Exception as e:
        return templates.TemplateResponse(
            request,
            "partials/error.html",
            {"message": _safe_message(e)},
        )

    return templates.TemplateResponse(
        request,
        "partials/meta_design.html",
        {"design": design},
    )


@app.post("/ui/meta-execute", response_class=HTMLResponse)
async def ui_meta_execute(
    request: Request,
    design_json: str = Form(...),
):
    try:
        design_data = _parse_json_payload(design_json)
    except json.JSONDecodeError as e:
        return templates.TemplateResponse(
            request,
            "partials/error.html",
            {"message": "Use a valid JSON object for the design."},
        )

    try:
        result = await run_in_threadpool(_execute_meta_chain_design, design_data)
    except HTTPException as e:
        return templates.TemplateResponse(
            request,
            "partials/error.html",
            {"message": e.detail},
        )
    except Exception as e:
        return templates.TemplateResponse(
            request,
            "partials/error.html",
            {"message": _safe_message(e)},
        )

    return templates.TemplateResponse(
        request,
        "partials/meta_execute.html",
        {"result": result},
    )


@app.get("/ui/artifacts", response_class=HTMLResponse)
async def ui_artifacts(request: Request):
    try:
        data = await list_artifacts()
    except HTTPException as e:
        return templates.TemplateResponse(
            request,
            "partials/error.html",
            {"message": e.detail},
        )
    return templates.TemplateResponse(
        request,
        "partials/artifacts.html",
        {"artifacts": data},
    )


@app.get("/ui/artifacts/{topic}/{filename}", response_class=HTMLResponse)
async def ui_artifact_detail(request: Request, topic: str, filename: str):
    try:
        data = await get_artifact(topic, filename)
    except HTTPException as e:
        return templates.TemplateResponse(
            request,
            "partials/error.html",
            {"message": e.detail},
        )

    return templates.TemplateResponse(
        request,
        "partials/artifact_detail.html",
        {"artifact": data, "topic": topic, "filename": filename},
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
