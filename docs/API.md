# API Reference

Base URL: `/api`

Interactive docs: `/docs`

## Foods

### List foods

`GET /api/foods/`

Query params:
- `search` (optional): substring match on name
- `category` (optional): exact category match

Response: `200 OK` → `FoodItemResponse[]`

### Get food by id

`GET /api/foods/{food_id}`

Response:
- `200 OK` → `FoodItemResponse`
- `404 Not Found`

### Create food

`POST /api/foods/`

Body:
```json
{
  "name": "Chicken Breast",
  "protein_per_100g": 31.0,
  "category": "meat",
  "serving_size_grams": 50.0,
  "serving_name": "piece"
}
```

Response:
- `201 Created` → `FoodItemResponse`
- `409 Conflict` if the name already exists

### Update food

`PUT /api/foods/{food_id}`

Body (partial):
```json
{ "protein_per_100g": 32.0 }
```

Response:
- `200 OK` → `FoodItemResponse`
- `404 Not Found`
- `409 Conflict` if updating to a name that already exists

### Delete food

`DELETE /api/foods/{food_id}`

Response:
- `204 No Content`
- `404 Not Found`

## Entries

### List entries (actual only)

`GET /api/entries/`

Query params:
- `date` (optional): ISO date (`YYYY-MM-DD`)

Response: `200 OK` → `ProteinEntryResponse[]`

### List today’s entries (actual only)

`GET /api/entries/today`

Response: `200 OK` → `ProteinEntryResponse[]`

### Create entry (actual)

`POST /api/entries/`

Body:
```json
{
  "food_item_id": 1,
  "quantity": 200,
  "quantity_type": "grams",
  "is_simulation": false
}
```

Response:
- `201 Created` → `ProteinEntryResponse`
- `404 Not Found` if `food_item_id` does not exist

### Delete entry

`DELETE /api/entries/{entry_id}`

Response:
- `204 No Content`
- `404 Not Found`

## Simulation

Simulation entries are stored in the same table as entries, using `is_simulation=true`.

### List simulation entries

`GET /api/entries/simulation`

Response: `200 OK` → `ProteinEntryResponse[]`

### Create simulation entry

`POST /api/entries/simulation`

Body:
```json
{
  "food_item_id": 1,
  "quantity": 2,
  "quantity_type": "servings",
  "is_simulation": true
}
```

Response:
- `201 Created` → `ProteinEntryResponse`
- `404 Not Found`

### Clear simulation entries

`DELETE /api/entries/simulation`

Response: `204 No Content`

## Summary

### Today’s summary (actual only)

`GET /api/summary/today`

Response:
```json
{
  "date": "2026-01-27",
  "total_protein": 87.5,
  "goal": 150.0,
  "percentage": 58.3,
  "remaining": 62.5,
  "entry_count": 4
}
```

### History (actual only)

`GET /api/summary/history?days=14`

Response: list of day totals (most recent first)

### Simulation summary (actual + planned)

`GET /api/summary/simulation`

Response:
```json
{
  "date": "2026-01-27",
  "actual_protein": 87.5,
  "simulation_protein": 45.0,
  "combined_total": 132.5,
  "goal": 150.0,
  "percentage": 88.3
}
```

## Settings

### Get settings

`GET /api/settings/`

Creates default settings on first run.

### Update settings

`PUT /api/settings/`

Body:
```json
{ "daily_protein_goal": 180.0 }
```

Response: updated settings.
