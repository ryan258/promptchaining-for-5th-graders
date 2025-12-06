import os
import sys
import glob
import subprocess
import json
import logging
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.core.meta_chain_generator import MetaChainGenerator
from src.core.chain import MinimalChainable
from src.core.main import prompt as core_prompt
from src.enhancements.natural_reasoning import REASONING_PATTERNS
from src.enhancements.adversarial_chains import ADVERSARIAL_PATTERNS
from src.enhancements.emergence_measurement import measure_emergence

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Prompt Chaining Tools SPA")

# Allow local dev frontends to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
OUTPUT_MARKDOWN_MARKER = "✅ Timeline saved to:"

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

@app.get("/tools", response_model=List[Tool])
async def list_tools():
    """Scan the tools directory and return available tools."""
    tools = []
    # Find all .py files in tools/*/*.py
    pattern = os.path.join(TOOLS_DIR, "*", "*.py")
    for file_path in glob.glob(pattern):
        if "__init__" in file_path:
            continue
            
        category = os.path.basename(os.path.dirname(file_path))
        filename = os.path.basename(file_path)
        name = filename.replace(".py", "")
        
        # Extract description from docstring (simple approach)
        description = "No description available."
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                if '"""' in content:
                    # Very basic extraction of the first docstring
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
    
    # Sort by category then name
    tools.sort(key=lambda x: (x.category, x.name))
    return tools

@app.post("/run")
async def run_tool(request: RunRequest):
    """Execute a tool as a subprocess and return the output."""
    tool_path = os.path.join(TOOLS_DIR, request.category, f"{request.tool_name}.py")
    
    if not os.path.exists(tool_path):
        raise HTTPException(status_code=404, detail="Tool not found")

    # Construct command
    cmd = ["python3", tool_path, request.topic]
    if request.context:
        cmd.extend(["--context", request.context])

    logger.info(f"Running command: {' '.join(cmd)}")

    try:
        # Run the tool
        result = subprocess.run(
            cmd,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=300 # 5 minute timeout
        )

        if result.returncode != 0:
            return {
                "status": "error",
                "stdout": result.stdout,
                "stderr": result.stderr
            }

        # Parse stdout to find the output file
        output_content = ""
        output_type = "text"
        output_file = None

        for line in result.stdout.split("\n"):
            if OUTPUT_JSON_MARKER in line:
                output_file = line.split(OUTPUT_JSON_MARKER)[1].strip()
                output_type = "json"
            elif OUTPUT_MARKDOWN_MARKER in line:
                output_file = line.split(OUTPUT_MARKDOWN_MARKER)[1].strip()
                output_type = "markdown"

        if output_file and os.path.exists(output_file):
            with open(output_file, "r", encoding="utf-8") as f:
                output_content = f.read()
                if output_type == "json":
                    try:
                        output_content = json.loads(output_content)
                    except (json.JSONDecodeError, ValueError):
                        pass # Keep as string if parse fails
        else:
            # Fallback: return stdout if no file found
            output_content = result.stdout

        return {
            "status": "success",
            "output": output_content,
            "type": output_type,
            "logs": result.stdout
        }

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


@app.post("/patterns/{pattern_name}")
async def run_pattern(pattern_name: str, payload: Dict[str, Any] = Body(...)):
    """Execute a reasoning pattern and return structured output."""
    pattern = REASONING_PATTERNS.get(pattern_name)
    if not pattern:
        raise HTTPException(status_code=404, detail=f"Pattern '{pattern_name}' not found")

    kwargs = _build_pattern_kwargs(pattern_name, payload or {})

    try:
        result, metadata = pattern["function"](**kwargs)
    except Exception as e:
        logger.error(f"Error running pattern {pattern_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "status": "success",
        "pattern": pattern_name,
        "result": result,
        "metadata": metadata
    }


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


@app.post("/adversarial/{pattern_name}")
async def run_adversarial(pattern_name: str, payload: Dict[str, Any] = Body(...)):
    """Run adversarial reasoning flows (red vs blue, dialectical, etc.)."""
    pattern = ADVERSARIAL_PATTERNS.get(pattern_name)
    if not pattern:
        raise HTTPException(status_code=404, detail=f"Adversarial pattern '{pattern_name}' not found")

    kwargs = _build_adversarial_kwargs(pattern_name, payload or {})

    try:
        result, metadata = pattern["function"](**kwargs)
    except Exception as e:
        logger.error(f"Error running adversarial pattern {pattern_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "status": "success",
        "pattern": pattern_name,
        "result": result,
        "metadata": metadata
    }


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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
