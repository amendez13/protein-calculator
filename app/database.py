"""Async SQLAlchemy database setup."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from functools import lru_cache
from typing import TYPE_CHECKING

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import get_settings

if TYPE_CHECKING:
    from app.models.settings import UserSettings


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""


@lru_cache(maxsize=1)
def get_engine() -> AsyncEngine:
    settings = get_settings()
    return create_async_engine(settings.database_url, echo=settings.debug)


@lru_cache(maxsize=1)
def get_sessionmaker() -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(get_engine(), class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency yielding an async database session."""

    async with get_sessionmaker()() as session:
        yield session


async def init_db() -> None:
    """Create all tables for all registered models."""

    # Ensure all models are imported before metadata creation.
    # (This is intentionally inside the function to avoid import order issues.)
    import app.models  # noqa: F401

    async with get_engine().begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    async with get_sessionmaker()() as session:
        await ensure_settings(session)
        await seed_default_foods(session)


async def reset_database_state() -> None:
    """Dispose the engine and clear internal caches.

    This is primarily useful for tests that need to change `PROTEIN_DATABASE_URL`
    at runtime.
    """

    if get_engine.cache_info().currsize:
        engine = get_engine()
        await engine.dispose()
    get_sessionmaker.cache_clear()
    get_engine.cache_clear()


async def ensure_settings(session: AsyncSession) -> UserSettings:
    """Ensure the single settings row exists (id=1)."""

    from app.models.settings import UserSettings

    settings = await session.get(UserSettings, 1)
    if settings is not None:
        return settings

    settings = UserSettings(id=1, daily_protein_goal=150.0)
    session.add(settings)
    await session.commit()
    await session.refresh(settings)
    return settings


async def seed_default_foods(session: AsyncSession) -> int:
    """Seed a small default set of foods if the table is empty.

    Returns:
        Number of rows inserted.
    """

    from app.models.food_item import FoodItem
    from app.seed_data import DEFAULT_FOODS

    result = await session.execute(select(func.count()).select_from(FoodItem))
    count = int(result.scalar_one())
    if count > 0:
        return 0

    foods = [FoodItem(**food) for food in DEFAULT_FOODS]
    session.add_all(foods)
    await session.commit()
    return len(foods)
