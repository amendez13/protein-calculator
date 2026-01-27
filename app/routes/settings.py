"""Settings API."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.settings import SettingsResponse, SettingsUpdate
from app.services.settings_service import get_or_create_settings, update_settings

router = APIRouter(prefix="/api/settings", tags=["settings"])


@router.get("/", response_model=SettingsResponse)
async def get_settings(db: AsyncSession = Depends(get_db)) -> SettingsResponse:
    settings = await get_or_create_settings(db)
    return SettingsResponse.model_validate(settings)


@router.put("/", response_model=SettingsResponse)
async def put_settings(payload: SettingsUpdate, db: AsyncSession = Depends(get_db)) -> SettingsResponse:
    settings = await update_settings(db, goal=payload.daily_protein_goal)
    return SettingsResponse.model_validate(settings)
