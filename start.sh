#!/usr/bin/env bash
# Script to run the E-Courts API

echo "🚀 Starting E-Courts API..."
echo "📍 API will be available at: http://localhost:8000"
echo "📚 Documentation: http://localhost:8000/docs"
echo ""

# Check if uv is available, otherwise use standard python/uvicorn
if command -v uv &> /dev/null; then
    echo "Using uv..."
    uv run uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
else
    echo "Using uvicorn..."
    uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
fi
