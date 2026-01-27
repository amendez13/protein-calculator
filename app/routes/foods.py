"""Food items API."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.food_item import FoodItemCreate, FoodItemResponse, FoodItemUpdate
from app.services.food_service import create_food, delete_food, get_food_by_id, get_foods, update_food

router = APIRouter(prefix="/api/foods", tags=["foods"])


@router.get("/", response_model=list[FoodItemResponse])
async def list_foods(
    search: str | None = Query(default=None),
    category: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
) -> list[FoodItemResponse]:
    foods = await get_foods(db, search=search, category=category)
    return [FoodItemResponse.model_validate(food) for food in foods]


@router.get("/{food_id}", response_model=FoodItemResponse)
async def get_food(food_id: int, db: AsyncSession = Depends(get_db)) -> FoodItemResponse:
    food = await get_food_by_id(db, food_id)
    if food is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food item not found")
    return FoodItemResponse.model_validate(food)


@router.post("/", response_model=FoodItemResponse, status_code=status.HTTP_201_CREATED)
async def create_food_item(food: FoodItemCreate, db: AsyncSession = Depends(get_db)) -> FoodItemResponse:
    try:
        created = await create_food(db, food)
        return FoodItemResponse.model_validate(created)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.put("/{food_id}", response_model=FoodItemResponse)
async def update_food_item(food_id: int, food: FoodItemUpdate, db: AsyncSession = Depends(get_db)) -> FoodItemResponse:
    try:
        updated = await update_food(db, food_id, food)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food item not found")
    return FoodItemResponse.model_validate(updated)


@router.delete("/{food_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_food_item(food_id: int, db: AsyncSession = Depends(get_db)) -> None:
    deleted = await delete_food(db, food_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food item not found")
