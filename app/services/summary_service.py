"""Summary/statistics calculations."""

from __future__ import annotations

from datetime import date as Date
from datetime import timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import ensure_settings
from app.models.protein_entry import ProteinEntry
from app.models.settings import UserSettings


async def get_daily_total(db: AsyncSession, target_date: Date) -> float:
    result = await db.execute(
        select(func.sum(ProteinEntry.protein_amount))
        .where(ProteinEntry.date == target_date)
        .where(ProteinEntry.is_simulation.is_(False)),
    )
    total = result.scalar_one_or_none()
    return float(total) if total is not None else 0.0


async def get_simulation_total(db: AsyncSession, target_date: Date) -> float:
    result = await db.execute(
        select(func.sum(ProteinEntry.protein_amount))
        .where(ProteinEntry.date == target_date)
        .where(ProteinEntry.is_simulation.is_(True)),
    )
    total = result.scalar_one_or_none()
    return float(total) if total is not None else 0.0


async def get_goal(db: AsyncSession) -> float:
    settings: UserSettings = await ensure_settings(db)
    return float(settings.daily_protein_goal)


def _percentage(total: float, goal: float) -> float:
    if goal <= 0:
        return 0.0
    return round((total / goal) * 100.0, 1)


async def get_today_summary(db: AsyncSession) -> dict[str, object]:
    today = Date.today()
    goal = await get_goal(db)

    total = round(await get_daily_total(db, today), 1)
    percentage = _percentage(total, goal)
    remaining = round(max(goal - total, 0.0), 1)

    count_result = await db.execute(
        select(func.count())
        .select_from(ProteinEntry)
        .where(ProteinEntry.date == today)
        .where(ProteinEntry.is_simulation.is_(False)),
    )
    entry_count = int(count_result.scalar_one())

    return {
        "date": today.isoformat(),
        "total_protein": total,
        "goal": goal,
        "percentage": percentage,
        "remaining": remaining,
        "entry_count": entry_count,
    }


async def get_history(db: AsyncSession, *, days: int) -> list[dict[str, object]]:
    today = Date.today()
    start = today - timedelta(days=days - 1)
    goal = await get_goal(db)

    result = await db.execute(
        select(ProteinEntry.date, func.sum(ProteinEntry.protein_amount))
        .where(ProteinEntry.date >= start)
        .where(ProteinEntry.is_simulation.is_(False))
        .group_by(ProteinEntry.date),
    )

    totals_by_date: dict[Date, float] = {row[0]: float(row[1] or 0.0) for row in result.all()}

    history: list[dict[str, object]] = []
    for offset in range(days):
        day = today - timedelta(days=offset)
        history.append(
            {
                "date": day.isoformat(),
                "total_protein": round(totals_by_date.get(day, 0.0), 1),
                "goal": goal,
            }
        )
    return history


async def get_simulation_summary(db: AsyncSession) -> dict[str, object]:
    today = Date.today()
    goal = await get_goal(db)

    actual = round(await get_daily_total(db, today), 1)
    simulated = round(await get_simulation_total(db, today), 1)
    combined = round(actual + simulated, 1)

    return {
        "date": today.isoformat(),
        "actual_protein": actual,
        "simulation_protein": simulated,
        "combined_total": combined,
        "goal": goal,
        "percentage": _percentage(combined, goal),
    }
