# Justfile for e-court-scraper
# Install just: https://github.com/casey/just

# List all available commands
default:
    @just --list

# Install/sync all dependencies
install:
    uv sync

# Run the API server
run:
    uv run python -m uvicorn api.main:app --reload

# Run the API server on all interfaces
serve:
    uv run python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Run the main.py script
demo:
    uv run python main.py

# Add a new dependency
add package:
    uv add {{package}}

# Add a dev dependency
add-dev package:
    uv add --dev {{package}}

# Update all dependencies
update:
    uv sync --upgrade

# Show dependency tree
tree:
    uv tree

# Clean up cache and temporary files
clean:
    rm -rf __pycache__ */__pycache__ */*/__pycache__
    rm -rf .pytest_cache
    rm -rf *.egg-info
    find . -name "*.pyc" -delete

# Format code with ruff (if added as dev dependency)
format:
    uv run ruff format .

# Lint code with ruff (if added as dev dependency)
lint:
    uv run ruff check .

# Run with production settings
prod:
    uv run uvicorn api.main:app --host 0.0.0.0 --port 8000 --workers 4
