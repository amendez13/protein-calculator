"""Tests for ProteinEntry model and schemas."""

from __future__ import annotations

from datetime import date, datetime

import pytest
from pydantic import ValidationError

from app.models.food_item import FoodItem
from app.models.protein_entry import ProteinEntry, QuantityType
from app.schemas.protein_entry import ProteinEntryCreate, ProteinEntryResponse


def test_protein_entry_create_validates() -> None:
    payload = ProteinEntryCreate(food_item_id=123, quantity=100.0, quantity_type=QuantityType.GRAMS, is_simulation=False)
    assert payload.food_item_id == 123
    assert payload.quantity_type == QuantityType.GRAMS


def test_protein_entry_create_rejects_non_positive_quantity() -> None:
    with pytest.raises(ValidationError):
        ProteinEntryCreate(food_item_id=1, quantity=0)


def test_protein_entry_response_from_orm() -> None:
    now = datetime.utcnow()

    food = FoodItem(name="Greek Yogurt", protein_per_100g=10.0, serving_size_grams=170.0, serving_name="cup", category="dairy")
    food.id = 5
    food.created_at = now

    entry = ProteinEntry(
        food_item_id=food.id,
        quantity=170.0,
        quantity_type=QuantityType.GRAMS,
        protein_amount=17.0,
        logged_at=now,
        date=date.today(),
        is_simulation=False,
        created_at=now,
    )
    entry.id = 99
    entry.food_item = food

    response = ProteinEntryResponse.model_validate(entry)
    assert response.id == 99
    assert response.food_item.name == "Greek Yogurt"
    assert response.protein_amount == 17.0
