# Setup Guide

This guide walks you through setting up protein-calculator for development or usage.

## Prerequisites

- Python 3.12 or higher
- pip (Python package installer)
- git

### Optional

- [List optional dependencies]

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/alex3m6/protein-calculator.git
cd protein-calculator
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate   # On Windows
```

### 3. Install Dependencies

```bash
# Install production dependencies
pip install -r requirements.txt

# Install development dependencies (optional)
pip install -r requirements-dev.txt
```

### 4. Configure the Application

```bash
# Optional: configure via environment variables
export PROTEIN_DATABASE_URL="sqlite+aiosqlite:///./protein.db"
export PROTEIN_DEBUG="false"
```

### 5. Verify Installation

```bash
# Run tests to verify setup
pytest

# Or run the application
uvicorn app.main:app --reload
```

## Configuration

### Environment Variables

You can also configure the application using environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `PROTEIN_DATABASE_URL` | Database URL | `sqlite+aiosqlite:///./protein.db` |
| `PROTEIN_DEBUG` | Enable SQLAlchemy echo | `false` |

## Development Setup

### Install Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Verify hooks work
pre-commit run --all-files
```

### IDE Setup

#### VS Code

Recommended extensions:
- Python
- Pylance
- Black Formatter
- isort

Settings (`.vscode/settings.json`):
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "[python]": {
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        }
    }
}
```

#### PyCharm

1. Set Python interpreter to `./venv/bin/python`
2. Enable Black formatter
3. Enable isort for imports

## Troubleshooting

### Common Issues

**Virtual environment not activated**
```bash
source venv/bin/activate
```

**Dependencies not installed**
```bash
pip install -r requirements.txt
```

**Pre-commit hooks not running**
```bash
pre-commit install
```

**Database path / permissions**

Set a writable SQLite path via:
```bash
export PROTEIN_DATABASE_URL="sqlite+aiosqlite:////absolute/path/to/protein.db"
```

### Getting Help

- Check the [Documentation Index](INDEX.md)
- Review [CI documentation](CI.md) for testing issues
- Open an issue on GitHub
