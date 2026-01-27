"""Async SQLAlchemy database setup."""

from __future__ import annotations

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import get_settings


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""


_settings = get_settings()

engine = create_async_engine(_settings.database_url, echo=_settings.debug)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency yielding an async database session."""

    async with async_session() as session:
        yield session


async def init_db() -> None:
    """Create all tables for all registered models."""

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
