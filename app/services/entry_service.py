"""Protein entry business logic."""

from __future__ import annotations

from datetime import date as Date
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.food_item import FoodItem
from app.models.protein_entry import ProteinEntry, QuantityType
from app.schemas.protein_entry import ProteinEntryCreate


def calculate_protein(food_item: FoodItem, quantity: float, quantity_type: QuantityType) -> float:
    if quantity_type == QuantityType.SERVINGS and food_item.serving_size_grams:
        grams = quantity * food_item.serving_size_grams
    else:
        grams = quantity
    return round(grams * food_item.protein_per_100g / 100.0, 1)


async def get_entries(db: AsyncSession, *, entry_date: Date | None = None) -> list[ProteinEntry]:
    statement = (
        select(ProteinEntry)
        .options(selectinload(ProteinEntry.food_item))
        .where(ProteinEntry.is_simulation.is_(False))
        .order_by(ProteinEntry.logged_at.desc())
    )
    if entry_date is not None:
        statement = statement.where(ProteinEntry.date == entry_date)

    result = await db.execute(statement)
    return list(result.scalars().all())


async def create_entry(db: AsyncSession, entry: ProteinEntryCreate) -> ProteinEntry:
    food_item = await db.get(FoodItem, entry.food_item_id)
    if food_item is None:
        raise LookupError("Food item not found")

    now = datetime.utcnow()
    protein_amount = calculate_protein(food_item, entry.quantity, entry.quantity_type)

    db_entry = ProteinEntry(
        food_item_id=entry.food_item_id,
        quantity=entry.quantity,
        quantity_type=entry.quantity_type,
        protein_amount=protein_amount,
        logged_at=now,
        date=now.date(),
        is_simulation=False,
        created_at=now,
    )
    db_entry.food_item = food_item
    db.add(db_entry)
    await db.commit()
    return db_entry


async def delete_entry(db: AsyncSession, entry_id: int) -> bool:
    entry = await db.get(ProteinEntry, entry_id)
    if entry is None:
        return False

    await db.delete(entry)
    await db.commit()
    return True
