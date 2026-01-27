"""Integration tests for /api/foods endpoints."""

from __future__ import annotations

import httpx
import pytest


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


@pytest.mark.anyio
async def test_list_foods_filters_by_category(api_client: httpx.AsyncClient) -> None:
    created = await api_client.post(
        "/api/foods/",
        json={"name": "Category Food", "protein_per_100g": 9.0, "category": "test-cat"},
    )
    assert created.status_code == 201

    filtered = await api_client.get("/api/foods/", params={"category": "test-cat"})
    assert filtered.status_code == 200
    assert any(food["name"] == "Category Food" for food in filtered.json())
