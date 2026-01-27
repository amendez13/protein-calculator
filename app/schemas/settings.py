"""Pydantic schemas for user settings."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SettingsUpdate(BaseModel):
    daily_protein_goal: float = Field(gt=0, le=500)


class SettingsResponse(BaseModel):
    id: int
    daily_protein_goal: float
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
