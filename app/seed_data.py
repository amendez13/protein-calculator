"""Default seed data.

This file contains a curated list of common high-protein foods for first-run seeding.
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
    # Meat & poultry
    {"name": "Chicken Breast", "protein_per_100g": 31.0, "category": "meat"},
    {"name": "Chicken Thigh", "protein_per_100g": 26.0, "category": "meat"},
    {"name": "Turkey Breast", "protein_per_100g": 29.0, "category": "meat"},
    {"name": "Ground Beef (90% lean)", "protein_per_100g": 26.0, "category": "meat"},
    {"name": "Pork Tenderloin", "protein_per_100g": 26.0, "category": "meat"},
    {"name": "Beef Steak", "protein_per_100g": 25.0, "category": "meat"},
    # Fish & seafood
    {"name": "Salmon", "protein_per_100g": 20.0, "category": "fish"},
    {"name": "Tuna (canned in water)", "protein_per_100g": 26.0, "category": "fish"},
    {"name": "Shrimp", "protein_per_100g": 24.0, "category": "fish"},
    {"name": "Cod", "protein_per_100g": 18.0, "category": "fish"},
    {"name": "Tilapia", "protein_per_100g": 26.0, "category": "fish"},
    # Dairy & eggs
    {"name": "Egg", "protein_per_100g": 13.0, "serving_size_grams": 50.0, "serving_name": "egg", "category": "dairy"},
    {
        "name": "Greek Yogurt",
        "protein_per_100g": 10.0,
        "serving_size_grams": 170.0,
        "serving_name": "cup",
        "category": "dairy",
    },
    {
        "name": "Cottage Cheese",
        "protein_per_100g": 11.0,
        "serving_size_grams": 113.0,
        "serving_name": "1/2 cup",
        "category": "dairy",
    },
    {"name": "Cheddar Cheese", "protein_per_100g": 25.0, "category": "dairy"},
    {"name": "Milk", "protein_per_100g": 3.4, "serving_size_grams": 240.0, "serving_name": "cup", "category": "dairy"},
    # Plant-based
    {"name": "Tofu", "protein_per_100g": 8.0, "category": "plant"},
    {"name": "Tempeh", "protein_per_100g": 19.0, "category": "plant"},
    {"name": "Edamame", "protein_per_100g": 11.0, "category": "plant"},
    {"name": "Lentils (cooked)", "protein_per_100g": 9.0, "category": "plant"},
    {"name": "Chickpeas (cooked)", "protein_per_100g": 9.0, "category": "plant"},
    {"name": "Black Beans (cooked)", "protein_per_100g": 9.0, "category": "plant"},
    {"name": "Quinoa (cooked)", "protein_per_100g": 4.0, "category": "plant"},
    # Nuts, seeds, and grains
    {"name": "Almonds", "protein_per_100g": 21.0, "category": "nuts"},
    {"name": "Pumpkin Seeds", "protein_per_100g": 30.0, "category": "nuts"},
    {
        "name": "Peanut Butter",
        "protein_per_100g": 25.0,
        "serving_size_grams": 32.0,
        "serving_name": "2 tbsp",
        "category": "nuts",
    },
    {
        "name": "Oats (dry)",
        "protein_per_100g": 17.0,
        "serving_size_grams": 40.0,
        "serving_name": "1/2 cup",
        "category": "grain",
    },
    # Supplements
    {
        "name": "Whey Protein Powder",
        "protein_per_100g": 80.0,
        "serving_size_grams": 30.0,
        "serving_name": "scoop",
        "category": "supplement",
    },
]
