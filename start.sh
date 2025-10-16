#!/usr/bin/env bash
# Script to run the E-Courts API with uv

echo "🚀 Starting E-Courts API with uv..."
echo "📍 API will be available at: http://localhost:8000"
echo "📚 Documentation: http://localhost:8000/docs"
echo ""

uv run python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
