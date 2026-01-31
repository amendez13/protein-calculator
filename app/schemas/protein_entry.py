"""Pydantic schemas for ProteinEntry."""

from __future__ import annotations

from datetime import date as Date
from datetime import datetime as DateTime

from pydantic import BaseModel, ConfigDict, Field

from app.models.protein_entry import QuantityType
from app.schemas.food_item import FoodItemResponse


class ProteinEntryCreate(BaseModel):
    food_item_id: int
    quantity: float = Field(gt=0)
    quantity_type: QuantityType = QuantityType.GRAMS
    is_simulation: bool = False


class ProteinEntryUpdate(BaseModel):
    food_item_id: int | None = None
    quantity: float | None = Field(default=None, gt=0)
    quantity_type: QuantityType | None = None
    date: Date | None = None


class ProteinEntryResponse(BaseModel):
    id: int
    food_item_id: int
    food_item: FoodItemResponse
    quantity: float
    quantity_type: QuantityType
    protein_amount: float
    logged_at: DateTime
    date: Date
    is_simulation: bool
    created_at: DateTime

    model_config = ConfigDict(from_attributes=True)
