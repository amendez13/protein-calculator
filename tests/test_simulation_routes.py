"""Integration tests for simulation endpoints."""

from __future__ import annotations

import httpx
import pytest


async def _get_food_id_by_name(client: httpx.AsyncClient, name: str) -> int:
    response = await client.get("/api/foods/", params={"search": name})
    response.raise_for_status()
    foods = response.json()
    for food in foods:
        if food["name"] == name:
            return int(food["id"])
    raise AssertionError(f"Seed food not found: {name}")


@pytest.mark.anyio
async def test_simulation_entries_and_summary(api_client: httpx.AsyncClient) -> None:
    chicken_id = await _get_food_id_by_name(api_client, "Chicken Breast")
    egg_id = await _get_food_id_by_name(api_client, "Egg")

    actual = await api_client.post(
        "/api/entries/",
        json={"food_item_id": chicken_id, "quantity": 100.0, "quantity_type": "grams"},
    )
    assert actual.status_code == 201

    sim = await api_client.post(
        "/api/entries/simulation",
        json={"food_item_id": egg_id, "quantity": 2.0, "quantity_type": "servings"},
    )
    assert sim.status_code == 201

    regular = await api_client.get("/api/entries/")
    assert regular.status_code == 200
    assert all(entry["is_simulation"] is False for entry in regular.json())

    sim_list = await api_client.get("/api/entries/simulation")
    assert sim_list.status_code == 200
    assert all(entry["is_simulation"] is True for entry in sim_list.json())

    summary = await api_client.get("/api/summary/simulation")
    assert summary.status_code == 200
    payload = summary.json()
    assert payload["actual_protein"] == 31.0
    assert payload["simulation_protein"] == 13.0
    assert payload["combined_total"] == 44.0

    cleared = await api_client.delete("/api/entries/simulation")
    assert cleared.status_code == 204

    sim_list = await api_client.get("/api/entries/simulation")
    assert sim_list.status_code == 200
    assert sim_list.json() == []
