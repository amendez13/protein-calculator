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
    application = FastAPI(title="Protein Calculator", lifespan=lifespan)

    from app.routes.entries import router as entries_router
    from app.routes.foods import router as foods_router
    from app.routes.settings import router as settings_router
    from app.routes.summary import router as summary_router

    application.include_router(entries_router)
    application.include_router(foods_router)
    application.include_router(settings_router)
    application.include_router(summary_router)
    return application


app = create_app()
