"""Tests for the FastAPI app entrypoint."""

from __future__ import annotations

import asyncio
from pathlib import Path

import pytest

from app import config as config_module
from app import database as database_module
from app.main import app


class TestSampleData:
    """Tests demonstrating fixture usage."""

    def test_sample_data_has_key(self, sample_data: dict) -> None:
        """Test that sample_data fixture has expected key."""
        assert "key" in sample_data
        assert sample_data["key"] == "value"

    def test_sample_data_has_number(self, sample_data: dict) -> None:
        """Test that sample_data fixture has expected number."""
        assert sample_data["number"] == 42


def test_app_lifespan_initializes_db(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    asyncio.run(database_module.reset_database_state())
    config_module.get_settings.cache_clear()
    db_path = tmp_path / "protein.db"
    monkeypatch.setenv("PROTEIN_DATABASE_URL", f"sqlite+aiosqlite:///{db_path}")

    async def _run() -> None:
        async with app.router.lifespan_context(app):
            pass

    try:
        asyncio.run(_run())
        assert db_path.exists()
    finally:
        asyncio.run(database_module.reset_database_state())
