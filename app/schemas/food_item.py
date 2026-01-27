"""Pydantic schemas for FoodItem."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class FoodItemBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    protein_per_100g: float = Field(ge=0)
    serving_size_grams: float | None = Field(default=None, gt=0)
    serving_name: str | None = Field(default=None, min_length=1, max_length=50)
    category: str | None = Field(default=None, min_length=1, max_length=50)


class FoodItemCreate(FoodItemBase):
    pass


class FoodItemUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    protein_per_100g: float | None = Field(default=None, ge=0)
    serving_size_grams: float | None = Field(default=None, gt=0)
    serving_name: str | None = Field(default=None, min_length=1, max_length=50)
    category: str | None = Field(default=None, min_length=1, max_length=50)


class FoodItemResponse(FoodItemBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
