import os
import sys
import glob
import subprocess
import json
import logging
from fastapi import FastAPI, HTTPException, Body, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Prompt Chaining Tools")

TEMPLATES_DIR = os.path.join(PROJECT_ROOT, "server", "templates")
STATIC_DIR = os.path.join(PROJECT_ROOT, "server", "static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

def _pretty_json(data: Any) -> str:
    if isinstance(data, str):
        return data
    try:
        return json.dumps(data, indent=2, ensure_ascii=False)
    except TypeError:
        return str(data)

templates.env.filters["pretty_json"] = _pretty_json

TOOLS_DIR = os.path.join(PROJECT_ROOT, 'tools')
ARTIFACTS_DIR = os.path.join(PROJECT_ROOT, 'artifacts')

class Tool(BaseModel):
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
    context: Dict[str, Any] = Field(default_factory=dict, max_items=20)
    constraints: List[str] = Field(default_factory=list, max_items=30)


class MetaExecuteRequest(BaseModel):
    design: Dict[str, Any]

OUTPUT_JSON_MARKER = "✅ Saved JSON to:"
OUTPUT_LOG_MARKERS = [
    "✅ Log saved to:",
    "✅ Timeline saved to:",
]

def _build_pattern_kwargs(pattern_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize incoming payloads to the expected pattern function args."""
    if pattern_name == "scientific_method":
        hypothesis = payload.get("hypothesis") or payload.get("topic")
        if not hypothesis:
            raise HTTPException(status_code=400, detail="hypothesis is required for scientific_method")
        return {
            "hypothesis": hypothesis,
            "context": payload.get("context", ""),
            "evidence_sources": payload.get("evidence_sources")
        }

    if pattern_name == "socratic_dialogue":
        belief = payload.get("belief") or payload.get("topic")
        if not belief:
            raise HTTPException(status_code=400, detail="belief is required for socratic_dialogue")
        return {
            "belief": belief,
            "teacher_persona": payload.get("teacher_persona", "Philosopher"),
            "depth": int(payload.get("depth", 5))
        }

    if pattern_name == "design_thinking":
        problem = payload.get("problem") or payload.get("topic")
        if not problem:
            raise HTTPException(status_code=400, detail="problem is required for design_thinking")
        return {
            "problem": problem,
            "target_user": payload.get("target_user", "End user"),
            "constraints": payload.get("constraints")
        }

    if pattern_name == "judicial_reasoning":
        case = payload.get("case") or payload.get("topic")
        if not case:
            raise HTTPException(status_code=400, detail="case is required for judicial_reasoning")
        return {
            "case": case,
            "relevant_principles": payload.get("relevant_principles"),
            "precedents": payload.get("precedents")
        }

    if pattern_name == "five_whys":
        problem = payload.get("problem") or payload.get("topic")
        if not problem:
            raise HTTPException(status_code=400, detail="problem is required for five_whys")
        return {
            "problem": problem,
            "depth": int(payload.get("depth", 5)),
            "context": payload.get("context", "")
        }

    raise HTTPException(status_code=404, detail=f"Pattern '{pattern_name}' not supported")


def _build_adversarial_kwargs(pattern_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize adversarial pattern inputs."""
    if pattern_name == "red_vs_blue":
        topic = payload.get("topic")
        position = payload.get("position_to_defend") or payload.get("position")
        if not topic or not position:
            raise HTTPException(status_code=400, detail="topic and position_to_defend are required for red_vs_blue")
        return {
            "topic": topic,
            "position_to_defend": position,
            "rounds": payload.get("rounds", 3),
            "judge_criteria": payload.get("judge_criteria")
        }

    if pattern_name == "dialectical":
        thesis = payload.get("thesis") or payload.get("topic")
        if not thesis:
            raise HTTPException(status_code=400, detail="thesis is required for dialectical")
        return {
            "thesis": thesis,
            "context": payload.get("context", ""),
            "domain": payload.get("domain", "")
        }

    if pattern_name == "adversarial_socratic":
        claim = payload.get("claim") or payload.get("topic")
        if not claim:
            raise HTTPException(status_code=400, detail="claim is required for adversarial_socratic")
        return {
            "claim": claim,
            "depth": payload.get("depth", 4),
            "aggressive": payload.get("aggressive", True)
        }

    raise HTTPException(status_code=404, detail=f"Adversarial pattern '{pattern_name}' not supported")


EMERGENCE_CHAIN_FUNCTIONS = {
    "scientific_method": lambda topic, **kwargs: REASONING_PATTERNS["scientific_method"]["function"](
        hypothesis=topic,
        context=kwargs.get("context", ""),
        evidence_sources=kwargs.get("evidence_sources")
    ),
    "design_thinking": lambda topic, **kwargs: REASONING_PATTERNS["design_thinking"]["function"](
        problem=topic,
        target_user=kwargs.get("target_user", "End user"),
        constraints=kwargs.get("constraints")
    ),
    "five_whys": lambda topic, **kwargs: REASONING_PATTERNS["five_whys"]["function"](
        problem=topic,
        depth=int(kwargs.get("depth", 5)),
        context=kwargs.get("context", "")
    ),
    "socratic_dialogue": lambda topic, **kwargs: REASONING_PATTERNS["socratic_dialogue"]["function"](
        belief=topic,
        teacher_persona=kwargs.get("teacher_persona", "Philosopher"),
        depth=int(kwargs.get("depth", 5))
    ),
    "judicial_reasoning": lambda topic, **kwargs: REASONING_PATTERNS["judicial_reasoning"]["function"](
        case=topic,
        relevant_principles=kwargs.get("relevant_principles"),
        precedents=kwargs.get("precedents")
    )
}

def _scan_tools() -> List[Tool]:
    """Scan the tools directory and return available tools."""
    tools = []
    pattern = os.path.join(TOOLS_DIR, "*", "*.py")
    for file_path in glob.glob(pattern):
        if "__init__" in file_path:
            continue

        category = os.path.basename(os.path.dirname(file_path))
        filename = os.path.basename(file_path)
        name = filename.replace(".py", "")

        description = "No description available."
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                if '"""' in content:
                    parts = content.split('"""')
                    if len(parts) >= 3:
                        description = parts[1].strip().split("\n")[0]
        except (IOError, UnicodeDecodeError):
            pass

        tools.append(Tool(
            name=name,
            category=category,
            path=file_path,
            description=description
        ))

    tools.sort(key=lambda x: (x.category, x.name))
    return tools


def _resolve_tool_path(category: str, tool_name: str) -> Optional[str]:
    """Return a verified tool path for known tools."""
    for tool in _scan_tools():
        if tool.category == category and tool.name == tool_name:
            return tool.path
    return None

@app.get("/tools", response_model=List[Tool])
async def list_tools():
    """Scan the tools directory and return available tools."""
    return _scan_tools()

def _execute_tool(category: str, tool_name: str, topic: str, context: Optional[str] = "") -> Dict[str, Any]:
    tool_path = _resolve_tool_path(category, tool_name)
    if not tool_path or not os.path.exists(tool_path):
        raise HTTPException(status_code=404, detail="Tool not found")

    cmd = ["python3", tool_path, topic]
    if context:
        cmd.extend(["--context", context])

    logger.info("Running command: %s", " ".join(cmd))

    result = subprocess.run(
        cmd,
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        timeout=300,
    )

    if result.returncode != 0:
        return {
            "status": "error",
            "stdout": result.stdout,
            "stderr": result.stderr,
        }

    output_content = ""
    output_type = "text"
    output_file = None

    for line in result.stdout.split("\n"):
        if OUTPUT_JSON_MARKER in line:
            output_file = line.split(OUTPUT_JSON_MARKER)[1].strip()
            output_type = "json"
        else:
            for marker in OUTPUT_LOG_MARKERS:
                if marker in line:
                    output_file = line.split(marker)[1].strip()
                    output_type = "markdown"
                    break

    if output_file and not os.path.isabs(output_file):
        output_file = os.path.join(PROJECT_ROOT, output_file)

    if output_file and os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as f:
            output_content = f.read()
            if output_type == "json":
                try:
                    output_content = json.loads(output_content)
                except (json.JSONDecodeError, ValueError):
                    pass
    else:
        output_content = result.stdout

    return {
        "status": "success",
        "output": output_content,
        "type": output_type,
        "logs": result.stdout,
    }

@app.post("/run")
async def run_tool(request: RunRequest):
    """Execute a tool as a subprocess and return the output."""
    try:
        return _execute_tool(request.category, request.tool_name, request.topic, request.context)
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Tool execution timed out")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
    pattern = REASONING_PATTERNS.get(pattern_name)
    if not pattern:
        raise HTTPException(status_code=404, detail=f"Pattern '{pattern_name}' not found")

    kwargs = _build_pattern_kwargs(pattern_name, payload or {})
    result, metadata = pattern["function"](**kwargs)

    return {
        "status": "success",
        "pattern": pattern_name,
        "result": result,
        "metadata": metadata,
    }

@app.post("/patterns/{pattern_name}")
async def run_pattern(pattern_name: str, payload: Dict[str, Any] = Body(...)):
    """Execute a reasoning pattern and return structured output."""
    try:
        return _execute_pattern(pattern_name, payload or {})
    except Exception as e:
        logger.error(f"Error running pattern {pattern_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


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
    pattern = ADVERSARIAL_PATTERNS.get(pattern_name)
    if not pattern:
        raise HTTPException(status_code=404, detail=f"Adversarial pattern '{pattern_name}' not found")

    kwargs = _build_adversarial_kwargs(pattern_name, payload or {})
    result, metadata = pattern["function"](**kwargs)

    return {
        "status": "success",
        "pattern": pattern_name,
        "result": result,
        "metadata": metadata,
    }

@app.post("/adversarial/{pattern_name}")
async def run_adversarial(pattern_name: str, payload: Dict[str, Any] = Body(...)):
    """Run adversarial reasoning flows (red vs blue, dialectical, etc.)."""
    try:
        return _execute_adversarial(pattern_name, payload or {})
    except Exception as e:
        logger.error(f"Error running adversarial pattern {pattern_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/meta-chain/design")
async def design_meta_chain(request: MetaDesignRequest):
    """Generate a chain design using the meta-chain generator."""
    generator = MetaChainGenerator()
    try:
        design = generator.design_chain(request.goal, request.context, request.constraints)
    except Exception as e:
        logger.error(f"Error designing meta-chain: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "status": "success",
        "design": design.to_dict()
    }


@app.post("/meta-chain/execute")
async def execute_meta_chain(request: MetaExecuteRequest):
    """Execute a previously designed chain and return the execution trace."""
    design_data = request.design or {}
    prompts = design_data.get("prompts") or []
    if not prompts:
        raise HTTPException(status_code=400, detail="Design must include prompts to execute")

    generator = MetaChainGenerator()
    try:
        outputs, filled_prompts, usage, trace = MinimalChainable.run(
            context=design_data.get("context") or {},
            model=generator.model_info,
            callable=core_prompt,
            prompts=prompts,
            return_trace=True,
            artifact_store=generator.artifact_store,
            topic=design_data.get("goal", "meta_chain_run").lower().replace(" ", "_")[:50]
        )
    except Exception as e:
        logger.error(f"Error executing meta-chain: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    trace["final_result"] = outputs[-1] if outputs else None

    return {
        "status": "success",
        "execution_trace": trace,
        "outputs": outputs,
        "prompts": filled_prompts,
        "usage": usage
    }


@app.post("/emergence/compare")
async def compare_emergence(payload: Dict[str, Any] = Body(...)):
    """Compare chain vs baseline outputs to measure emergence."""
    topic = payload.get("topic")
    if not topic:
        raise HTTPException(status_code=400, detail="topic is required for emergence comparison")

    chain_name = payload.get("chain_name", "scientific_method")
    chain_kwargs = payload.get("chain_kwargs") or {}
    chain_func = EMERGENCE_CHAIN_FUNCTIONS.get(chain_name)
    if not chain_func:
        raise HTTPException(
            status_code=404,
            detail=f"Chain '{chain_name}' not supported for emergence. Available: {', '.join(EMERGENCE_CHAIN_FUNCTIONS.keys())}"
        )

    baseline_prompt = payload.get("baseline_prompt")

    try:
        comparison, metadata = measure_emergence(
            topic=topic,
            chain_function=chain_func,
            baseline_prompt=baseline_prompt,
            **chain_kwargs
        )
    except Exception as e:
        logger.error(f"Error measuring emergence for {chain_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "status": "success",
        "comparison": comparison,
        "metadata": metadata
    }

@app.get("/artifacts")
async def list_artifacts():
    """List all artifacts in the artifacts directory."""
    if not os.path.exists(ARTIFACTS_DIR):
        return []

    artifacts = []
    try:
        for topic in os.listdir(ARTIFACTS_DIR):
            topic_path = os.path.join(ARTIFACTS_DIR, topic)
            if not os.path.isdir(topic_path) or topic.startswith('.'):
                continue

            # Get artifact files in this topic
            for filename in os.listdir(topic_path):
                if filename.startswith('.'):
                    continue

                file_path = os.path.join(topic_path, filename)
                if os.path.isfile(file_path):
                    stat = os.stat(file_path)
                    artifacts.append({
                        "topic": topic,
                        "filename": filename,
                        "path": file_path,
                        "size": stat.st_size,
                        "modified": stat.st_mtime
                    })
    except Exception as e:
        logger.error(f"Error listing artifacts: {e}")

    # Sort by modified time (newest first)
    artifacts.sort(key=lambda x: x["modified"], reverse=True)
    return artifacts

@app.get("/artifacts/{topic}/{filename}")
async def get_artifact(topic: str, filename: str):
    """Get the content of a specific artifact."""
    file_path = os.path.join(ARTIFACTS_DIR, topic, filename)

    if not os.path.exists(file_path):
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
    file_path = os.path.join(ARTIFACTS_DIR, topic, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Artifact not found")

    try:
        os.remove(file_path)

        # Remove topic directory if empty
        topic_path = os.path.join(ARTIFACTS_DIR, topic)
        if os.path.isdir(topic_path) and not os.listdir(topic_path):
            os.rmdir(topic_path)

        return {"status": "success", "message": "Artifact deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def _group_tools_by_category(tools: List[Tool]) -> Dict[str, List[Tool]]:
    grouped: Dict[str, List[Tool]] = {}
    for tool in tools:
        grouped.setdefault(tool.category, []).append(tool)
    return grouped


@app.get("/", response_class=HTMLResponse)
async def ui_index(request: Request):
    tools = _scan_tools()
    reasoning = [
        {
            "name": name,
            "description": info.get("description", ""),
            "use_when": info.get("use_when", ""),
            "example": info.get("example", ""),
        }
        for name, info in REASONING_PATTERNS.items()
    ]
    adversarial = [
        {
            "name": name,
            "description": info.get("description", ""),
            "use_when": info.get("use_when", ""),
            "example": info.get("example", ""),
        }
        for name, info in ADVERSARIAL_PATTERNS.items()
    ]

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "tools_by_category": _group_tools_by_category(tools),
            "reasoning_patterns": reasoning,
            "adversarial_patterns": adversarial,
        },
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
            "partials/error.html",
            {"request": request, "message": "Invalid tool selection."},
        )

    category, tool_name = tool_key.split(":", 1)

    try:
        result = _execute_tool(category, tool_name, topic, context)
    except Exception as e:
        return templates.TemplateResponse(
            "partials/error.html",
            {"request": request, "message": f"Tool run failed: {e}"},
        )

    return templates.TemplateResponse(
        "partials/tool_result.html",
        {"request": request, "result": result},
    )


def _parse_json_payload(payload_json: str) -> Dict[str, Any]:
    payload_json = (payload_json or "").strip()
    if not payload_json:
        return {}
    return json.loads(payload_json)


@app.post("/ui/run-pattern", response_class=HTMLResponse)
async def ui_run_pattern(
    request: Request,
    pattern_name: str = Form(...),
    topic: str = Form(""),
    payload_json: str = Form(""),
):
    try:
        payload = _parse_json_payload(payload_json)
    except json.JSONDecodeError as e:
        return templates.TemplateResponse(
            "partials/error.html",
            {"request": request, "message": f"Invalid JSON payload: {e}"},
        )

    if not payload and topic:
        payload = {"topic": topic}

    try:
        result = _execute_pattern(pattern_name, payload)
    except Exception as e:
        return templates.TemplateResponse(
            "partials/error.html",
            {"request": request, "message": f"Pattern failed: {e}"},
        )

    return templates.TemplateResponse(
        "partials/pattern_result.html",
        {"request": request, "result": result},
    )


@app.post("/ui/run-adversarial", response_class=HTMLResponse)
async def ui_run_adversarial(
    request: Request,
    pattern_name: str = Form(...),
    topic: str = Form(""),
    payload_json: str = Form(""),
):
    try:
        payload = _parse_json_payload(payload_json)
    except json.JSONDecodeError as e:
        return templates.TemplateResponse(
            "partials/error.html",
            {"request": request, "message": f"Invalid JSON payload: {e}"},
        )

    if not payload and topic:
        payload = {"topic": topic}

    try:
        result = _execute_adversarial(pattern_name, payload)
    except Exception as e:
        return templates.TemplateResponse(
            "partials/error.html",
            {"request": request, "message": f"Adversarial run failed: {e}"},
        )

    return templates.TemplateResponse(
        "partials/pattern_result.html",
        {"request": request, "result": result},
    )


@app.post("/ui/meta-design", response_class=HTMLResponse)
async def ui_meta_design(
    request: Request,
    goal: str = Form(...),
    context_json: str = Form(""),
    constraints: str = Form(""),
):
    try:
        context = _parse_json_payload(context_json)
    except json.JSONDecodeError as e:
        return templates.TemplateResponse(
            "partials/error.html",
            {"request": request, "message": f"Invalid context JSON: {e}"},
        )

    constraint_list = []
    if constraints:
        for item in constraints.replace(",", "\n").splitlines():
            item = item.strip()
            if item:
                constraint_list.append(item)

    generator = MetaChainGenerator()
    try:
        design = generator.design_chain(goal, context, constraint_list)
    except Exception as e:
        return templates.TemplateResponse(
            "partials/error.html",
            {"request": request, "message": f"Meta-chain design failed: {e}"},
        )

    return templates.TemplateResponse(
        "partials/meta_design.html",
        {"request": request, "design": design.to_dict()},
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
            "partials/error.html",
            {"request": request, "message": f"Invalid design JSON: {e}"},
        )

    prompts = design_data.get("prompts") or []
    if not prompts:
        return templates.TemplateResponse(
            "partials/error.html",
            {"request": request, "message": "Design must include prompts to execute."},
        )

    generator = MetaChainGenerator()
    try:
        outputs, filled_prompts, usage, trace = MinimalChainable.run(
            context=design_data.get("context") or {},
            model=generator.model_info,
            callable=core_prompt,
            prompts=prompts,
            return_trace=True,
            artifact_store=generator.artifact_store,
            topic=design_data.get("goal", "meta_chain_run").lower().replace(" ", "_")[:50],
        )
    except Exception as e:
        return templates.TemplateResponse(
            "partials/error.html",
            {"request": request, "message": f"Meta-chain execute failed: {e}"},
        )

    trace["final_result"] = outputs[-1] if outputs else None

    result = {
        "status": "success",
        "execution_trace": trace,
        "outputs": outputs,
        "prompts": filled_prompts,
        "usage": usage,
    }

    return templates.TemplateResponse(
        "partials/meta_execute.html",
        {"request": request, "result": result},
    )


@app.get("/ui/artifacts", response_class=HTMLResponse)
async def ui_artifacts(request: Request):
    data = await list_artifacts()
    return templates.TemplateResponse(
        "partials/artifacts.html",
        {"request": request, "artifacts": data},
    )


@app.get("/ui/artifacts/{topic}/{filename}", response_class=HTMLResponse)
async def ui_artifact_detail(request: Request, topic: str, filename: str):
    try:
        data = await get_artifact(topic, filename)
    except HTTPException as e:
        return templates.TemplateResponse(
            "partials/error.html",
            {"request": request, "message": e.detail},
        )

    return templates.TemplateResponse(
        "partials/artifact_detail.html",
        {"request": request, "artifact": data, "topic": topic, "filename": filename},
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
