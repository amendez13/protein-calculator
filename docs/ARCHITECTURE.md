# Architecture

This document describes the technical architecture of `protein-calculator`.

## System Overview

```
┌───────────────┐       ┌─────────────────────────────┐
│   Browser     │       │            FastAPI           │
│  (SPA UI)     │──────▶│  app/main.py (routers + UI)  │
└───────┬───────┘       └──────────────┬──────────────┘
        │                               │
        │  /static/*                    │ /api/*
        │                               ▼
        │                      ┌───────────────────────┐
        │                      │   Routes (app/routes) │
        │                      └──────────┬────────────┘
        │                                 ▼
        │                      ┌───────────────────────┐
        │                      │ Services (app/services)│
        │                      └──────────┬────────────┘
        │                                 ▼
        │                      ┌───────────────────────┐
        └──────────────────────│ Async SQLAlchemy +     │
                               │ SQLite (protein.db)    │
                               └───────────────────────┘
```

## Key Modules

- `app/main.py`: FastAPI app creation, lifespan DB init, static mounting (`/static`) and root (`/`).
- `app/config.py`: environment-driven settings (`PROTEIN_DATABASE_URL`, `PROTEIN_DEBUG`).
- `app/database.py`: engine/session factory, `get_db()` dependency, `init_db()` table creation + seed + default settings.
- `app/models/*`: SQLAlchemy models (`FoodItem`, `ProteinEntry`, `UserSettings`).
- `app/schemas/*`: Pydantic request/response models.
- `app/routes/*`: API endpoints grouped by domain.
- `app/services/*`: business logic and DB queries.
- `app/static/*`: single-page frontend (HTML/CSS/JS).

## Database Schema

### ER Diagram (high level)

```
FoodItem (food_items) 1 ──── * ProteinEntry (protein_entries)

UserSettings (user_settings)  (single row, id=1)
```

### Tables

**`food_items`**
- `id` (PK)
- `name` (unique)
- `protein_per_100g` (float)
- `serving_size_grams` (nullable float)
- `serving_name` (nullable string)
- `category` (nullable string)
- `created_at` (datetime)

**`protein_entries`**
- `id` (PK)
- `food_item_id` (FK → `food_items.id`)
- `quantity` (float)
- `quantity_type` (`grams` | `servings`)
- `protein_amount` (float; stored as computed at write time)
- `logged_at` (datetime)
- `date` (date; indexed for daily summaries)
- `is_simulation` (bool; simulation/planning entries)
- `created_at` (datetime)

**`user_settings`**
- `id` (PK; expected `1`)
- `daily_protein_goal` (float)
- `updated_at` (datetime)

## API Surface

The API is mounted under `/api/*`. See `docs/API.md` for the full reference, or browse the interactive Swagger UI at `/docs`.

Key groups:
- Foods: `app/routes/foods.py`
- Entries (+ simulation): `app/routes/entries.py`
- Summary/history (+ simulation): `app/routes/summary.py`
- Settings: `app/routes/settings.py`

## Frontend Structure

The UI is a static SPA served by FastAPI:

- `/` → `app/static/index.html`
- `/static/css/styles.css` → styling, including the progress wheel
- `/static/js/app.js` → client-side state, tab navigation, and API calls

## Data Flow

### Log an entry (Today)

1. UI searches foods: `GET /api/foods/?search=...`
2. UI submits log form: `POST /api/entries/`
3. Server:
   - loads the chosen `FoodItem`
   - computes `protein_amount` (grams vs servings)
   - persists a `ProteinEntry` (non-simulation)
4. UI refreshes:
   - `GET /api/entries/today` to render today’s list
   - `GET /api/summary/today` to update wheel/goal

### Simulation (planning)

1. UI adds planned items via `POST /api/entries/simulation`
2. UI refreshes `GET /api/entries/simulation` and `GET /api/summary/simulation`
3. Remove a single planned item via `DELETE /api/entries/simulation/{entry_id}`
4. “Clear planned” uses `DELETE /api/entries/simulation`

## Design Decisions

- Single-user app: settings stored in one row (`user_settings.id=1`).
- Store computed `protein_amount` on `ProteinEntry` to simplify summaries and reduce repeated calculations.
- Treat simulations as flagged `ProteinEntry` rows (`is_simulation=true`) to reuse the same schema and joins.
- Seed data only runs when `food_items` is empty (first run behavior).

## Testing

Tests live in `tests/` and include:
- Integration tests hitting the ASGI app via `httpx` transport
- Service-layer smoke coverage to keep CI coverage stable
