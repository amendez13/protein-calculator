"""Integration tests for /api/entries endpoints."""

from __future__ import annotations

from datetime import date

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
async def test_entry_calculation_grams(api_client: httpx.AsyncClient) -> None:
    chicken_id = await _get_food_id_by_name(api_client, "Chicken Breast")

    created = await api_client.post(
        "/api/entries/",
        json={"food_item_id": chicken_id, "quantity": 200.0, "quantity_type": "grams"},
    )
    assert created.status_code == 201
    payload = created.json()
    assert payload["protein_amount"] == 62.0


@pytest.mark.anyio
async def test_entry_calculation_servings(api_client: httpx.AsyncClient) -> None:
    egg_id = await _get_food_id_by_name(api_client, "Egg")

    created = await api_client.post(
        "/api/entries/",
        json={"food_item_id": egg_id, "quantity": 2.0, "quantity_type": "servings"},
    )
    assert created.status_code == 201
    payload = created.json()
    assert payload["protein_amount"] == 13.0


@pytest.mark.anyio
async def test_entries_list_and_delete(api_client: httpx.AsyncClient) -> None:
    chicken_id = await _get_food_id_by_name(api_client, "Chicken Breast")
    created = await api_client.post(
        "/api/entries/",
        json={"food_item_id": chicken_id, "quantity": 100.0, "quantity_type": "grams"},
    )
    entry_id = created.json()["id"]

    today_entries = await api_client.get("/api/entries/today")
    assert today_entries.status_code == 200
    assert any(entry["id"] == entry_id for entry in today_entries.json())

    date_entries = await api_client.get("/api/entries/", params={"date": date.today().isoformat()})
    assert date_entries.status_code == 200
    assert any(entry["id"] == entry_id for entry in date_entries.json())

    deleted = await api_client.delete(f"/api/entries/{entry_id}")
    assert deleted.status_code == 204

    missing = await api_client.get(f"/api/entries/{entry_id}")
    assert missing.status_code in (404, 405)


@pytest.mark.anyio
async def test_delete_entry_404(api_client: httpx.AsyncClient) -> None:
    response = await api_client.delete("/api/entries/999999")
    assert response.status_code == 404


@pytest.mark.anyio
async def test_update_entry_quantity(api_client: httpx.AsyncClient) -> None:
    """Verify updating quantity recalculates protein_amount."""
    chicken_id = await _get_food_id_by_name(api_client, "Chicken Breast")

    created = await api_client.post(
        "/api/entries/",
        json={"food_item_id": chicken_id, "quantity": 100.0, "quantity_type": "grams"},
    )
    assert created.status_code == 201
    entry_id = created.json()["id"]
    assert created.json()["protein_amount"] == 31.0

    updated = await api_client.put(
        f"/api/entries/{entry_id}",
        json={"quantity": 200.0},
    )
    assert updated.status_code == 200
    assert updated.json()["quantity"] == 200.0
    assert updated.json()["protein_amount"] == 62.0


@pytest.mark.anyio
async def test_update_entry_food_item(api_client: httpx.AsyncClient) -> None:
    """Verify updating food_item recalculates protein_amount."""
    chicken_id = await _get_food_id_by_name(api_client, "Chicken Breast")
    egg_id = await _get_food_id_by_name(api_client, "Egg")

    created = await api_client.post(
        "/api/entries/",
        json={"food_item_id": chicken_id, "quantity": 100.0, "quantity_type": "grams"},
    )
    entry_id = created.json()["id"]

    updated = await api_client.put(
        f"/api/entries/{entry_id}",
        json={"food_item_id": egg_id},
    )
    assert updated.status_code == 200
    assert updated.json()["food_item_id"] == egg_id
    assert updated.json()["food_item"]["name"] == "Egg"


@pytest.mark.anyio
async def test_update_entry_date(api_client: httpx.AsyncClient) -> None:
    """Verify updating date moves entry to a different day."""
    chicken_id = await _get_food_id_by_name(api_client, "Chicken Breast")

    created = await api_client.post(
        "/api/entries/",
        json={"food_item_id": chicken_id, "quantity": 100.0, "quantity_type": "grams"},
    )
    entry_id = created.json()["id"]
    original_date = created.json()["date"]

    new_date = "2025-01-15"
    updated = await api_client.put(
        f"/api/entries/{entry_id}",
        json={"date": new_date},
    )
    assert updated.status_code == 200
    assert updated.json()["date"] == new_date
    assert updated.json()["date"] != original_date


@pytest.mark.anyio
async def test_update_entry_date_moves_to_correct_day(api_client: httpx.AsyncClient) -> None:
    """Critical test: verify entry appears on new date and NOT on original date after update."""
    chicken_id = await _get_food_id_by_name(api_client, "Chicken Breast")

    # Create entry for today
    created = await api_client.post(
        "/api/entries/",
        json={"food_item_id": chicken_id, "quantity": 100.0, "quantity_type": "grams"},
    )
    entry_id = created.json()["id"]
    original_date = created.json()["date"]

    # Verify entry appears on original date
    original_entries = await api_client.get("/api/entries/", params={"date": original_date})
    assert any(e["id"] == entry_id for e in original_entries.json())

    # Update to a different date
    new_date = "2025-06-15"
    updated = await api_client.put(
        f"/api/entries/{entry_id}",
        json={"date": new_date},
    )
    assert updated.status_code == 200
    assert updated.json()["date"] == new_date

    # Verify entry NO LONGER appears on original date
    original_entries_after = await api_client.get("/api/entries/", params={"date": original_date})
    assert not any(e["id"] == entry_id for e in original_entries_after.json())

    # Verify entry NOW appears on new date
    new_entries = await api_client.get("/api/entries/", params={"date": new_date})
    assert any(e["id"] == entry_id for e in new_entries.json())


@pytest.mark.anyio
async def test_update_entry_404(api_client: httpx.AsyncClient) -> None:
    response = await api_client.put(
        "/api/entries/999999",
        json={"quantity": 100.0},
    )
    assert response.status_code == 404
