"""Tests for database configuration and initialization."""

from __future__ import annotations

import asyncio
import importlib
from pathlib import Path

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app import config as config_module


def _sqlite_url(db_path: Path) -> str:
    return f"sqlite+aiosqlite:///{db_path}"


def test_get_settings_reads_env(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    config_module.get_settings.cache_clear()
    expected_url = _sqlite_url(tmp_path / "test.db")
    monkeypatch.setenv("PROTEIN_DATABASE_URL", expected_url)

    settings = config_module.get_settings()
    assert settings.database_url == expected_url


def test_init_db_creates_sqlite_file(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    config_module.get_settings.cache_clear()
    db_path = tmp_path / "protein.db"
    monkeypatch.setenv("PROTEIN_DATABASE_URL", _sqlite_url(db_path))

    import app.database as database_module

    database_module = importlib.reload(database_module)

    asyncio.run(database_module.init_db())
    try:
        assert db_path.exists()
    finally:
        asyncio.run(database_module.engine.dispose())


def test_get_db_yields_session(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    config_module.get_settings.cache_clear()
    monkeypatch.setenv("PROTEIN_DATABASE_URL", _sqlite_url(tmp_path / "sessions.db"))

    import app.database as database_module

    database_module = importlib.reload(database_module)

    async def _run() -> None:
        async for session in database_module.get_db():
            assert isinstance(session, AsyncSession)
            break

    try:
        asyncio.run(_run())
    finally:
        asyncio.run(database_module.engine.dispose())
