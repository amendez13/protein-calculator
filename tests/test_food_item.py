"""Tests for FoodItem model and schemas."""

from __future__ import annotations

from datetime import datetime

import pytest
from pydantic import ValidationError

from app.models.food_item import FoodItem
from app.schemas.food_item import FoodItemCreate, FoodItemResponse, FoodItemUpdate


def test_food_item_create_validates() -> None:
    model = FoodItemCreate(
        name="Chicken Breast",
        protein_per_100g=31.0,
        serving_size_grams=50.0,
        serving_name="piece",
        category="meat",
    )
    assert model.name == "Chicken Breast"
    assert model.protein_per_100g == 31.0


def test_food_item_create_rejects_empty_name() -> None:
    with pytest.raises(ValidationError):
        FoodItemCreate(name="", protein_per_100g=10.0)


def test_food_item_update_allows_partial() -> None:
    patch = FoodItemUpdate(protein_per_100g=25.0)
    assert patch.protein_per_100g == 25.0
    assert patch.name is None


def test_food_item_response_from_orm() -> None:
    food = FoodItem(name="Egg", protein_per_100g=13.0, serving_size_grams=50.0, serving_name="egg", category="dairy")
    food.id = 1
    food.created_at = datetime.utcnow()

    response = FoodItemResponse.model_validate(food)
    assert response.id == 1
    assert response.name == "Egg"
