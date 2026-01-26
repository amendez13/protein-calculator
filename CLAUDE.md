# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A FastAPI webapp that helps users log and count protein intake throughout the day

**Core workflow**: User logs protein intake entries (food name, protein grams) → App stores in SQLite → User views daily totals and history

**Deployment**: Single-user app running on VPS with Tailscale (no public internet exposure, no complex auth needed)

## Constraints and Best Practices

* This project is documentation-driven. Before starting work, read:
  * README.md
  * docs/INDEX.md
* After finishing any task, update relevant documentation given changes in codebase.
* Pre-commit checks must pass before committing. If pre-commit doesn't run, investigate and fix.
** pyproject.toml, ci.yml and pre-commit-config.yaml have to have the same configuration so local pre-commit and CI checks behave in the same way.
** Any code quality exceptions must be properly documented with a comment in code.
* Branch naming: `feature/description`, `fix/description`, `docs/description`
* Commit messages: Use conventional commits (feat:, fix:, docs:, refactor:, test:, chore:)

## Architecture

### Technology Stack
- **Python**: 3.10+
- **FastAPI**: Web framework with automatic OpenAPI docs
- **SQLite + SQLAlchemy**: Lightweight database for single-user
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation

### Key Components
1. **API Routes** (`app/routes/`):
   - Entry endpoints: create, list, delete protein entries
   - Summary endpoints: daily/weekly totals

2. **Database Models** (`app/models/`):
   - ProteinEntry: food name, protein grams, timestamp
   - SQLite for persistence

3. **Services** (`app/services/`):
   - Business logic for calculations and aggregations

### Processing Strategy
- Async SQLAlchemy for database operations
- Simple REST API (no auth since Tailscale handles network security)
- Logging with Python's logging module

## Development Commands

### Initial Setup

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate   # On Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Copy and configure settings
cp config/config.example.yaml config/config.yaml
# Edit config/config.yaml with your settings
```

### Running Tests

```bash
# Activate virtual environment (if not already active)
source venv/bin/activate

# Run all tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=term-missing

# Run specific test file
pytest tests/test_main.py
```

### Common Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Update dependencies
pip install --upgrade -r requirements.txt

# Run linting
black app/
isort app/
flake8 app/
mypy app/

# Run security checks
bandit -r app/ -ll

# Deactivate virtual environment when done
deactivate
```

### Running the Application

```bash
# Activate virtual environment
source venv/bin/activate

# Run development server (auto-reload)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run production server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

API docs available at: http://localhost:8000/docs
