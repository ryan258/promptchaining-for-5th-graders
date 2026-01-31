#!/bin/bash

# Kill background processes on exit
trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT

echo "🚀 Starting Prompt Chaining App..."

# Start Backend
echo "🐍 Starting FastAPI Backend..."
if [ ! -f venv/bin/activate ]; then
    echo "❌ Virtual environment not found. Run 'python -m venv venv' first."
    exit 1
fi
source venv/bin/activate
uvicorn server.main:app --reload --port 8000
