"""Settings business logic."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.database import ensure_settings
from app.models.settings import UserSettings


async def get_or_create_settings(db: AsyncSession) -> UserSettings:
    return await ensure_settings(db)


async def update_settings(db: AsyncSession, *, goal: float) -> UserSettings:
    settings = await ensure_settings(db)
    settings.daily_protein_goal = goal
    await db.commit()
    await db.refresh(settings)
    return settings
