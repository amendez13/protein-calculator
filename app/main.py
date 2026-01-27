"""FastAPI application entry point."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    from app.database import init_db

    await init_db()
    yield


def create_app() -> FastAPI:
    return FastAPI(title="Protein Calculator", lifespan=lifespan)


app = create_app()
