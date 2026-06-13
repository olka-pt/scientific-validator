# backend/app/main.py

import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from backend.app.api.routes.upload import (
    REPORT_DIR,
    UPLOAD_DIR,
    cleanup_old_files,
    router as upload_router,
)


CLEANUP_INTERVAL_SECONDS = 5 * 60


async def cleanup_files_loop():
    while True:
        cleanup_old_files(
            UPLOAD_DIR
        )

        cleanup_old_files(
            REPORT_DIR
        )

        await asyncio.sleep(
            CLEANUP_INTERVAL_SECONDS
        )


@asynccontextmanager
async def lifespan(app: FastAPI):
    cleanup_task = asyncio.create_task(
        cleanup_files_loop()
    )

    try:
        yield
    finally:
        cleanup_task.cancel()

        try:
            await cleanup_task
        except asyncio.CancelledError:
            pass


app = FastAPI(
    title="Валидатор научных статей",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(
    upload_router
)


templates = Jinja2Templates(
    directory="backend/app/templates"
)


@app.get(
    "/",
    response_class=HTMLResponse,
)
async def root(
    request: Request,
):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={},
    )