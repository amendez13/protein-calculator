"""Protein entry model."""

from __future__ import annotations

from datetime import date, datetime
from enum import Enum

from sqlalchemy import Boolean, Date, DateTime
from sqlalchemy import Enum as SAEnum
from sqlalchemy import Float, ForeignKey, Index, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.food_item import FoodItem


class QuantityType(str, Enum):
    GRAMS = "grams"
    SERVINGS = "servings"


class ProteinEntry(Base):
    __tablename__ = "protein_entries"

    __table_args__ = (Index("ix_protein_entries_date_is_simulation", "date", "is_simulation"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    food_item_id: Mapped[int] = mapped_column(ForeignKey("food_items.id"), index=True)
    quantity: Mapped[float] = mapped_column(Float)
    quantity_type: Mapped[QuantityType] = mapped_column(
        SAEnum(QuantityType, name="quantity_type"),
        default=QuantityType.GRAMS,
    )
    protein_amount: Mapped[float] = mapped_column(Float)
    logged_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    date: Mapped[date] = mapped_column(Date, index=True, default=date.today)
    is_simulation: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    food_item: Mapped[FoodItem] = relationship(FoodItem)
