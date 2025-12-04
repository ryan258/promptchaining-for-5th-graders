#!/bin/bash

# Kill background processes on exit
trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT

echo "🚀 Starting Prompt Chaining SPA..."

# Start Backend
echo "🐍 Starting FastAPI Backend..."
if [ ! -f venv/bin/activate ]; then
    echo "❌ Virtual environment not found. Run 'python -m venv venv' first."
    exit 1
fi
source venv/bin/activate
uvicorn server.main:app --reload --port 8000 &
BACKEND_PID=$!

# Wait for backend to be ready (simple sleep for now)
sleep 2

# Start Frontend
echo "⚛️  Starting Vite Frontend..."
cd web
npm run dev &
FRONTEND_PID=$!

echo "✅ App is running!"
echo "   Backend: http://localhost:8000"
echo "   Frontend: http://localhost:5173"
echo "   Press Ctrl+C to stop."

wait
