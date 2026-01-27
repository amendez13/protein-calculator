"""Integration tests for /api/summary endpoints."""

from __future__ import annotations

from datetime import date

import httpx
import pytest


@pytest.mark.anyio
async def test_today_summary_calculates_totals(api_client: httpx.AsyncClient) -> None:
    foods = await api_client.get("/api/foods/", params={"search": "Chicken Breast"})
    chicken_id = foods.json()[0]["id"]

    await api_client.post(
        "/api/entries/",
        json={"food_item_id": chicken_id, "quantity": 100.0, "quantity_type": "grams"},
    )

    summary = await api_client.get("/api/summary/today")
    assert summary.status_code == 200
    payload = summary.json()

    assert payload["date"] == date.today().isoformat()
    assert payload["total_protein"] == 31.0
    assert payload["goal"] == 150.0
    assert payload["percentage"] == 20.7
    assert payload["remaining"] == 119.0
    assert payload["entry_count"] == 1


@pytest.mark.anyio
async def test_history_includes_today(api_client: httpx.AsyncClient) -> None:
    history = await api_client.get("/api/summary/history", params={"days": 3})
    assert history.status_code == 200
    items = history.json()
    assert len(items) == 3
    assert items[0]["date"] == date.today().isoformat()


@pytest.mark.anyio
async def test_today_summary_excludes_simulation_entries(api_client: httpx.AsyncClient) -> None:
    foods = await api_client.get("/api/foods/", params={"search": "Chicken Breast"})
    chicken_id = foods.json()[0]["id"]

    # Simulation entry should not count toward /today summary.
    sim = await api_client.post(
        "/api/entries/simulation",
        json={"food_item_id": chicken_id, "quantity": 100.0, "quantity_type": "grams"},
    )
    assert sim.status_code == 201

    summary = await api_client.get("/api/summary/today")
    assert summary.status_code == 200
    assert summary.json()["total_protein"] == 0.0
