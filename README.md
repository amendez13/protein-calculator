# protein-calculator

![CI](https://github.com/amendez13/protein-calculator/workflows/CI/badge.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Coverage](https://img.shields.io/badge/coverage-80%25-green.svg)

A FastAPI web app that helps you log and track protein intake throughout the day.

## Features

- Food database (seeded on first run)
- Log daily protein entries (grams or servings)
- Edit entries (change food, quantity, or date)
- Navigate between days to view/edit past entries
- Progress wheel (current vs goal)
- Simulation mode for "what-if" planning
- History view (daily totals)
- Settings: update daily protein goal, add foods

## Quick Start

### Prerequisites

- Python 3.10 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/amendez13/protein-calculator.git
cd protein-calculator
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate   # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the app:
```bash
uvicorn app.main:app --reload
```

### Usage

- App UI: `http://localhost:8000/`
- API docs (Swagger): `http://localhost:8000/docs`

## Configuration

Configuration is via environment variables:

- `PROTEIN_DATABASE_URL` (default: `sqlite+aiosqlite:///./protein.db`)
- `PROTEIN_DEBUG` (default: `false`, enables SQLAlchemy echo)

## Project Structure

```
protein-calculator/
├── .github/workflows/    # CI/CD configuration
├── .claude/              # Claude Code configuration
├── config/               # Configuration files
├── docs/                 # Documentation
├── app/       # Source code
├── tests/         # Test files
├── CLAUDE.md             # AI assistant guidance
├── README.md             # This file
├── pyproject.toml        # Tool configuration
└── requirements.txt      # Dependencies
```

## Development

### Setup Development Environment

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=term-missing
```

### Code Quality

This project uses:
- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking
- **bandit** for security scanning
- **pip-audit** for dependency vulnerability checking

All checks run automatically via pre-commit hooks and CI.

## CI/CD

GitHub Actions runs the following checks on every push and PR:

1. **Lint**: Black, isort, flake8, mypy
2. **Test**: pytest across Python 3.10, 3.11, 3.12
3. **Coverage**: 80% minimum coverage
4. **Security**: bandit and pip-audit

See [docs/CI.md](docs/CI.md) for details.

## Documentation

- [Documentation Index](docs/INDEX.md) - All documentation
- [Setup Guide](docs/SETUP.md) - Installation and configuration
- [CI Documentation](docs/CI.md) - CI/CD pipeline details
- [API Reference](docs/API.md) - Endpoints and examples
- [Deployment Guide](docs/DEPLOYMENT.md) - systemd/nginx/Tailscale notes

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting
5. Commit your changes (`git commit -m 'feat: add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

[Choose your license]

## Acknowledgments

- [Acknowledgment 1]
- [Acknowledgment 2]
