# Architecture Documentation

This document describes the technical architecture of protein-calculator.

## Overview

Protein Calculator is a FastAPI single-user web app with:

- An async SQLAlchemy + SQLite database
- A REST API under `/api/*`
- A static single-page frontend served from `app/static/`

This document evolves as features land; see each PR for incremental design notes.

## Configuration

Runtime config is provided via `app/config.py` using `pydantic-settings`.

- `PROTEIN_DATABASE_URL` (default: `sqlite+aiosqlite:///./protein.db`)
- `PROTEIN_DEBUG` (default: `false`, enables SQLAlchemy echo)

## Database

`app/database.py` owns engine/session lifecycle:

- `get_engine()`: cached async engine
- `get_sessionmaker()`: cached session factory (`async_sessionmaker`)
- `get_db()`: FastAPI dependency yielding an `AsyncSession`
- `init_db()`: creates all tables from `Base.metadata`, then ensures settings + seeds default foods

Seed data:

- `app/seed_data.py`: small starter list used by `seed_default_foods()`

Models live under `app/models/` and inherit from `app.database.Base`. The first model is:

- `FoodItem` (`food_items`): protein content per 100g plus optional serving metadata
- `ProteinEntry` (`protein_entries`): logged intake events (actual + simulation)
- `UserSettings` (`user_settings`): single-row config (protein goal)

## System Components

### Component Diagram

```
┌─────────────────┐     ┌─────────────────┐
│   Component A   │────▶│   Component B   │
└─────────────────┘     └─────────────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│   Component C   │     │   Component D   │
└─────────────────┘     └─────────────────┘
```

### Component A

**Purpose**: [Description]

**Responsibilities**:
- Responsibility 1
- Responsibility 2

**Key Files**:
- `app/component_a.py`

## API Layer

Routes are grouped under `app/routes/` and call into `app/services/` for business logic.

- `app/routes/foods.py`: `/api/foods` CRUD endpoints
- `app/services/food_service.py`: DB queries and mutations for food items
- `app/routes/entries.py`: `/api/entries` endpoints for logging intake
- `app/services/entry_service.py`: protein calculation + entry CRUD
- `app/routes/summary.py`: `/api/summary` endpoints (today + history)
- `app/services/summary_service.py`: daily totals and goal/percentage calculations
- `app/routes/settings.py`: `/api/settings` endpoints (get/update goal)
- `app/services/settings_service.py`: get-or-create and update logic for settings
- Simulation endpoints live under `/api/entries/simulation` and `/api/summary/simulation`.

### Component B

**Purpose**: [Description]

**Responsibilities**:
- Responsibility 1
- Responsibility 2

**Key Files**:
- `app/component_b.py`

## Data Flow

1. Step 1: [Description]
2. Step 2: [Description]
3. Step 3: [Description]

## Design Decisions

### Decision 1: [Title]

**Context**: [Why this decision was needed]

**Decision**: [What was decided]

**Consequences**:
- Pro: [Positive consequence]
- Con: [Negative consequence]

### Decision 2: [Title]

**Context**: [Why this decision was needed]

**Decision**: [What was decided]

**Consequences**:
- Pro: [Positive consequence]
- Con: [Negative consequence]

## Performance Considerations

- [Consideration 1]
- [Consideration 2]

## Security Considerations

- [Security measure 1]
- [Security measure 2]

## Future Enhancements

- [ ] Enhancement 1
- [ ] Enhancement 2
- [ ] Enhancement 3
