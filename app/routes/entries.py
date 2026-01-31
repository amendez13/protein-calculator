"""Protein entries API."""

from __future__ import annotations

from datetime import date as Date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.protein_entry import ProteinEntryCreate, ProteinEntryResponse
from app.services.entry_service import (
    clear_simulation_entries,
    create_entry,
    create_simulation_entry,
    delete_entry,
    delete_simulation_entry,
    get_entries,
    get_simulation_entries,
)

router = APIRouter(prefix="/api/entries", tags=["entries"])


@router.get("/", response_model=list[ProteinEntryResponse])
async def list_entries(
    entry_date: Date | None = Query(default=None, alias="date"),
    db: AsyncSession = Depends(get_db),
) -> list[ProteinEntryResponse]:
    entries = await get_entries(db, entry_date=entry_date)
    return [ProteinEntryResponse.model_validate(entry) for entry in entries]


@router.get("/today", response_model=list[ProteinEntryResponse])
async def get_today_entries(db: AsyncSession = Depends(get_db)) -> list[ProteinEntryResponse]:
    entries = await get_entries(db, entry_date=Date.today())
    return [ProteinEntryResponse.model_validate(entry) for entry in entries]


@router.post("/", response_model=ProteinEntryResponse, status_code=status.HTTP_201_CREATED)
async def create_protein_entry(entry: ProteinEntryCreate, db: AsyncSession = Depends(get_db)) -> ProteinEntryResponse:
    try:
        created = await create_entry(db, entry)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return ProteinEntryResponse.model_validate(created)


@router.get("/simulation", response_model=list[ProteinEntryResponse])
async def list_simulation_entries(db: AsyncSession = Depends(get_db)) -> list[ProteinEntryResponse]:
    entries = await get_simulation_entries(db)
    return [ProteinEntryResponse.model_validate(entry) for entry in entries]


@router.post("/simulation", response_model=ProteinEntryResponse, status_code=status.HTTP_201_CREATED)
async def create_simulation(entry: ProteinEntryCreate, db: AsyncSession = Depends(get_db)) -> ProteinEntryResponse:
    try:
        created = await create_simulation_entry(db, entry)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return ProteinEntryResponse.model_validate(created)


@router.delete("/simulation", status_code=status.HTTP_204_NO_CONTENT)
async def clear_simulation(db: AsyncSession = Depends(get_db)) -> None:
    await clear_simulation_entries(db)


@router.delete("/simulation/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_simulation_entry_by_id(entry_id: int, db: AsyncSession = Depends(get_db)) -> None:
    deleted = await delete_simulation_entry(db, entry_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Simulation entry not found")


@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_protein_entry(entry_id: int, db: AsyncSession = Depends(get_db)) -> None:
    deleted = await delete_entry(db, entry_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found")
