"""Service-layer smoke tests to keep coverage stable.

These tests exercise key business-logic paths directly (without ASGI transport)
so coverage stays representative across environments.
"""

from __future__ import annotations

import pytest

from app import config as config_module
from app import database as database_module
from app.models.protein_entry import QuantityType
from app.schemas.food_item import FoodItemCreate, FoodItemUpdate
from app.schemas.protein_entry import ProteinEntryCreate
from app.services import entry_service, food_service, settings_service, summary_service


@pytest.mark.anyio
async def test_services_smoke(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    await database_module.reset_database_state()
    config_module.get_settings.cache_clear()
    monkeypatch.setenv("PROTEIN_DATABASE_URL", f"sqlite+aiosqlite:///{tmp_path / 'services.db'}")

    await database_module.init_db()

    async with database_module.get_sessionmaker()() as db:
        foods = await food_service.get_foods(db)
        assert foods

        created_food = await food_service.create_food(
            db,
            FoodItemCreate(name="Service Food", protein_per_100g=50.0, category="test"),
        )
        assert created_food.id is not None

        updated_food = await food_service.update_food(db, created_food.id, FoodItemUpdate(protein_per_100g=55.0))
        assert updated_food is not None
        assert updated_food.protein_per_100g == 55.0

        entry = await entry_service.create_entry(
            db,
            ProteinEntryCreate(food_item_id=created_food.id, quantity=100.0, quantity_type=QuantityType.GRAMS),
        )
        assert entry.protein_amount == 55.0

        sim_entry = await entry_service.create_simulation_entry(
            db,
            ProteinEntryCreate(food_item_id=created_food.id, quantity=1.0, quantity_type=QuantityType.SERVINGS),
        )
        assert sim_entry.is_simulation is True

        assert await entry_service.get_entries(db)
        assert await entry_service.get_simulation_entries(db)

        await settings_service.update_settings(db, goal=200.0)
        today = await summary_service.get_today_summary(db)
        assert today["goal"] == 200.0

        sim_summary = await summary_service.get_simulation_summary(db)
        assert sim_summary["combined_total"] >= sim_summary["actual_protein"]

        assert await entry_service.clear_simulation_entries(db) >= 1

        assert await food_service.delete_food(db, created_food.id) is True

    await database_module.reset_database_state()
