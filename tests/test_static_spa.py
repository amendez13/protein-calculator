"""Integration tests for serving the static SPA."""

from __future__ import annotations

import httpx
import pytest


@pytest.mark.anyio
async def test_root_serves_index_html(api_client: httpx.AsyncClient) -> None:
    response = await api_client.get("/")
    assert response.status_code == 200
    assert "<title>Protein Calculator</title>" in response.text


@pytest.mark.anyio
async def test_static_assets_are_served(api_client: httpx.AsyncClient) -> None:
    css = await api_client.get("/static/css/styles.css")
    assert css.status_code == 200
    assert ".progress-wheel" in css.text

    js = await api_client.get("/static/js/app.js")
    assert js.status_code == 200
    assert "const App" in js.text
