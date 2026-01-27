"""Tests for UserSettings model and schemas."""

from __future__ import annotations

from datetime import datetime

import pytest
from pydantic import ValidationError

from app.models.settings import UserSettings
from app.schemas.settings import SettingsResponse, SettingsUpdate


def test_settings_update_validates_range() -> None:
    model = SettingsUpdate(daily_protein_goal=150.0)
    assert model.daily_protein_goal == 150.0

    with pytest.raises(ValidationError):
        SettingsUpdate(daily_protein_goal=0)

    with pytest.raises(ValidationError):
        SettingsUpdate(daily_protein_goal=501)


def test_settings_response_from_orm() -> None:
    now = datetime.utcnow()
    settings = UserSettings(id=1, daily_protein_goal=180.0, updated_at=now)
    response = SettingsResponse.model_validate(settings)
    assert response.id == 1
    assert response.daily_protein_goal == 180.0
