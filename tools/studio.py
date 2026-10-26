"""Short commands for one local workspace. Never sends a model request."""

import argparse
import importlib.util
import os
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def workspace_directory() -> Path:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env")
    return Path(os.getenv("PROMPT_STUDIO_DATA", str(ROOT / "workspace"))).expanduser().resolve()


def atomic_write(path: Path, text: str | bytes):
    path = path.expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise ValueError("That file already exists. Choose a new backup filename to preserve the existing copy.")
    descriptor, name = tempfile.mkstemp(prefix=".studio-backup-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(text.encode("utf-8") if isinstance(text, str) else text)
            stream.flush()
            os.fsync(stream.fileno())
        # Hard-link publication is atomic and refuses to overwrite a raced file.
        os.link(name, path)
    finally:
        Path(name).unlink(missing_ok=True)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Prompt Chaining Studio — one local thinking workbench")
    commands = parser.add_subparsers(dest="command")
    serve = commands.add_parser("start", help="Start at http://127.0.0.1:8000")
    serve.add_argument("--port", type=int, default=8000)
    commands.add_parser("doctor", help="Check local setup without API calls or tests")
    backup = commands.add_parser("backup", help="Export the workspace; defaults to a timestamped file")
    backup.add_argument("path", nargs="?")
    restore = commands.add_parser("restore", help="Add a Studio JSON backup without overwriting work")
    restore.add_argument("path")
    args = parser.parse_args(argv)
    command = args.command or "start"

    if command == "doctor":
        modules = ("fastapi", "uvicorn", "jinja2", "markdown_it", "multipart", "openai", "dotenv", "pydantic", "chromadb")
        missing = [name for name in modules if importlib.util.find_spec(name) is None]
        print(f"Python: {sys.version.split()[0]}")
        if missing:
            print("Missing dependencies: " + ", ".join(missing))
            print("Install with: python -m pip install -r requirements.txt")
            return 1
        from lib.core.llm_client import configured_model_names, get_prompt_settings, has_api_key
        try:
            models, settings = configured_model_names(), get_prompt_settings()
            print("Dependencies: available")
            print(f"Workspace: {workspace_directory()}")
            print("Live generation: " + ("key configured (not tested)" if has_api_key() else "add a key to .env when ready"))
            print("Models: " + ", ".join(models))
            print(f"Output token limit: {settings['max_tokens']} per step")
            print("No requests sent. This checks configuration, not provider access.")
            return 0
        except ValueError:
            print("Invalid configuration. Check model IDs, MAX_TOKENS, DEFAULT_TEMPERATURE and REQUEST_TIMEOUT_SECONDS in .env.")
            return 1

    if command == "start":
        import uvicorn
        port = getattr(args, "port", 8000)
        if not 1 <= port <= 65535:
            parser.error("port must be between 1 and 65535")
        print(f"Prompt Chaining Studio · http://127.0.0.1:{port}")
        print("Ctrl+C pauses after the current request, saves the answer, and stops.")
        uvicorn.run("server.main:app", host="127.0.0.1", port=port, workers=1)
        return 0

    from lib.workbench.store import Store
    store = Store(workspace_directory())
    try:
        if command == "backup":
            from datetime import datetime
            path = Path(args.path) if args.path else ROOT / "backups" / f"studio-{datetime.now():%Y%m%d-%H%M%S}.zip"
            if path.suffix.lower() not in {".json", ".zip"}:
                raise ValueError("Choose a .zip archive or a .json backup filename.")
            data = store.backup().model_dump_json(indent=2) if path.suffix.lower() == ".json" else store.archive()
            atomic_write(path, data)
            print(f"Workspace saved: {path.expanduser().resolve()}")
        elif command == "restore":
            with Path(args.path).expanduser().open("rb") as stream:
                from lib.workbench.backups import ARCHIVE_LIMIT
                raw = stream.read(ARCHIVE_LIMIT + 1)
            recipes, runs = store.restore(raw)
            print(f"Added {recipes} recipes and {runs} runs. Existing work was preserved. No requests sent.")
    except (ValueError, OSError) as exc:
        # Validation errors may include private source text; omit their payload.
        from pydantic import ValidationError
        print("Invalid Studio backup. No records were imported." if isinstance(exc, ValidationError) else str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
