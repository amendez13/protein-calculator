"""Summary and history API."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.summary_service import get_history, get_today_summary

router = APIRouter(prefix="/api/summary", tags=["summary"])


@router.get("/today")
async def today_summary(db: AsyncSession = Depends(get_db)) -> dict[str, object]:
    return await get_today_summary(db)


@router.get("/history")
async def history(
    days: int = Query(default=7, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
) -> list[dict[str, object]]:
    return await get_history(db, days=days)
