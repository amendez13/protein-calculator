"""Food item model."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class FoodItem(Base):
    __tablename__ = "food_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    protein_per_100g: Mapped[float] = mapped_column(Float)
    serving_size_grams: Mapped[float | None] = mapped_column(Float, nullable=True)
    serving_name: Mapped[str | None] = mapped_column(String(50), nullable=True)
    category: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
