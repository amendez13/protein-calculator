"""Pytest configuration and shared fixtures."""

from __future__ import annotations

import httpx
import pytest

from app import config as config_module
from app import database as database_module
from app.main import create_app


@pytest.fixture
def sample_data() -> dict:
    """Provide sample data for tests.

    Returns:
        A dictionary with sample test data.
    """
    return {
        "key": "value",
        "number": 42,
        "items": ["a", "b", "c"],
    }


@pytest.fixture
async def api_client(monkeypatch: pytest.MonkeyPatch, tmp_path):
    await database_module.reset_database_state()
    config_module.get_settings.cache_clear()
    monkeypatch.setenv("PROTEIN_DATABASE_URL", f"sqlite+aiosqlite:///{tmp_path / 'test.db'}")

    app = create_app()
    transport = httpx.ASGITransport(app=app)

    async with app.router.lifespan_context(app):
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            yield client

    await database_module.reset_database_state()
