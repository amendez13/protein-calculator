"""Integration tests for /api/foods endpoints."""

from __future__ import annotations

from pathlib import Path

import httpx
import pytest

from app import config as config_module
from app import database as database_module
from app.main import create_app


@pytest.fixture
async def api_client(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    await database_module.reset_database_state()
    config_module.get_settings.cache_clear()
    monkeypatch.setenv("PROTEIN_DATABASE_URL", f"sqlite+aiosqlite:///{tmp_path / 'test.db'}")

    app = create_app()
    transport = httpx.ASGITransport(app=app)

    async with app.router.lifespan_context(app):
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            yield client

    await database_module.reset_database_state()


@pytest.mark.anyio
async def test_list_foods_returns_seeded_rows(api_client: httpx.AsyncClient) -> None:
    response = await api_client.get("/api/foods/")
    assert response.status_code == 200
    foods = response.json()
    assert isinstance(foods, list)
    assert any(food["name"] == "Chicken Breast" for food in foods)


@pytest.mark.anyio
async def test_food_crud_happy_path(api_client: httpx.AsyncClient) -> None:
    create = await api_client.post(
        "/api/foods/",
        json={"name": "Test Food", "protein_per_100g": 12.5, "category": "test"},
    )
    assert create.status_code == 201
    created = create.json()
    food_id = created["id"]

    get_one = await api_client.get(f"/api/foods/{food_id}")
    assert get_one.status_code == 200
    assert get_one.json()["name"] == "Test Food"

    update = await api_client.put(
        f"/api/foods/{food_id}",
        json={"protein_per_100g": 15.0},
    )
    assert update.status_code == 200
    assert update.json()["protein_per_100g"] == 15.0

    filtered = await api_client.get("/api/foods/", params={"search": "test"})
    assert filtered.status_code == 200
    assert any(food["id"] == food_id for food in filtered.json())

    deleted = await api_client.delete(f"/api/foods/{food_id}")
    assert deleted.status_code == 204

    get_missing = await api_client.get(f"/api/foods/{food_id}")
    assert get_missing.status_code == 404


@pytest.mark.anyio
async def test_get_food_404(api_client: httpx.AsyncClient) -> None:
    response = await api_client.get("/api/foods/999999")
    assert response.status_code == 404
