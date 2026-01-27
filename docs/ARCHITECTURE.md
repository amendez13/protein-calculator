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

- `engine`: global async engine
- `async_session`: session factory (`async_sessionmaker`)
- `get_db()`: FastAPI dependency yielding an `AsyncSession`
- `init_db()`: creates all tables from `Base.metadata`

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
