import os
import glob
import subprocess
import json
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Prompt Chaining Tools SPA")

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TOOLS_DIR = os.path.join(PROJECT_ROOT, 'tools')

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

OUTPUT_JSON_MARKER = "✅ Saved JSON to:"
OUTPUT_MARKDOWN_MARKER = "✅ Timeline saved to:"

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
