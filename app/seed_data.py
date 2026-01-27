"""Default seed data.

This file intentionally contains a small starter set; the comprehensive list lives in
the dedicated seed issue.
"""

from __future__ import annotations

from typing_extensions import NotRequired, TypedDict


class FoodSeed(TypedDict):
    name: str
    protein_per_100g: float
    serving_size_grams: NotRequired[float]
    serving_name: NotRequired[str]
    category: NotRequired[str]


DEFAULT_FOODS: list[FoodSeed] = [
    {"name": "Chicken Breast", "protein_per_100g": 31.0, "category": "meat"},
    {"name": "Egg", "protein_per_100g": 13.0, "serving_size_grams": 50.0, "serving_name": "egg", "category": "dairy"},
    {
        "name": "Greek Yogurt",
        "protein_per_100g": 10.0,
        "serving_size_grams": 170.0,
        "serving_name": "cup",
        "category": "dairy",
    },
    {"name": "Salmon", "protein_per_100g": 20.0, "category": "fish"},
    {"name": "Tofu", "protein_per_100g": 8.0, "category": "plant"},
    {"name": "Whey Protein Powder", "protein_per_100g": 80.0, "serving_size_grams": 30.0, "serving_name": "scoop"},
]
