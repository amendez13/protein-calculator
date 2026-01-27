"""Integration tests for /api/settings endpoints."""

from __future__ import annotations

import httpx
import pytest


@pytest.mark.anyio
async def test_get_settings_creates_default(api_client: httpx.AsyncClient) -> None:
    response = await api_client.get("/api/settings/")
    assert response.status_code == 200
    payload = response.json()
    assert payload["id"] == 1
    assert payload["daily_protein_goal"] == 150.0


@pytest.mark.anyio
async def test_update_settings_persists(api_client: httpx.AsyncClient) -> None:
    updated = await api_client.put("/api/settings/", json={"daily_protein_goal": 180.0})
    assert updated.status_code == 200
    assert updated.json()["daily_protein_goal"] == 180.0

    reread = await api_client.get("/api/settings/")
    assert reread.status_code == 200
    assert reread.json()["daily_protein_goal"] == 180.0


@pytest.mark.anyio
async def test_update_settings_rejects_invalid(api_client: httpx.AsyncClient) -> None:
    bad = await api_client.put("/api/settings/", json={"daily_protein_goal": -10})
    assert bad.status_code == 422
