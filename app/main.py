from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from prometheus_fastapi_instrumentator import Instrumentator

from app.config import get_settings
from app.routes import invoices, payments


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="Duplo-style Payments API",
        description="Mock B2B invoice/payments service built as a DevOps portfolio project.",
        version=settings.app_version,
    )
    app.include_router(invoices.router)
    app.include_router(payments.router)
    frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
    app.mount("/app", StaticFiles(directory=frontend_dir, html=True), name="frontend")

    @app.get("/", include_in_schema=False)
    def frontend_home() -> RedirectResponse:
        return RedirectResponse(url="/app/")

    @app.get("/health", tags=["ops"])
    def health() -> dict[str, str]:
        return {"status": "ok", "version": settings.app_version, "env": settings.app_env}

    Instrumentator().instrument(app).expose(app, endpoint="/metrics", tags=["ops"])
    return app


app = create_app()
