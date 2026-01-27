"""Food item business logic."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.food_item import FoodItem
from app.schemas.food_item import FoodItemCreate, FoodItemUpdate


async def get_foods(db: AsyncSession, *, search: str | None = None, category: str | None = None) -> list[FoodItem]:
    statement = select(FoodItem).order_by(FoodItem.name.asc())
    if search:
        statement = statement.where(FoodItem.name.ilike(f"%{search}%"))
    if category:
        statement = statement.where(FoodItem.category == category)

    result = await db.execute(statement)
    return list(result.scalars().all())


async def get_food_by_id(db: AsyncSession, food_id: int) -> FoodItem | None:
    return await db.get(FoodItem, food_id)


async def create_food(db: AsyncSession, food_data: FoodItemCreate) -> FoodItem:
    existing = await db.execute(select(FoodItem).where(FoodItem.name == food_data.name))
    if existing.scalar_one_or_none() is not None:
        raise ValueError("Food item with this name already exists")

    food = FoodItem(**food_data.model_dump())
    db.add(food)
    await db.commit()
    await db.refresh(food)
    return food


async def update_food(db: AsyncSession, food_id: int, patch: FoodItemUpdate) -> FoodItem | None:
    food = await db.get(FoodItem, food_id)
    if food is None:
        return None

    data = patch.model_dump(exclude_unset=True)
    if "name" in data:
        existing = await db.execute(select(FoodItem).where(FoodItem.name == data["name"], FoodItem.id != food_id))
        if existing.scalar_one_or_none() is not None:
            raise ValueError("Food item with this name already exists")

    for key, value in data.items():
        setattr(food, key, value)

    await db.commit()
    await db.refresh(food)
    return food


async def delete_food(db: AsyncSession, food_id: int) -> bool:
    food = await db.get(FoodItem, food_id)
    if food is None:
        return False

    await db.delete(food)
    await db.commit()
    return True
