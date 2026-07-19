from fastapi import FastAPI
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

    @app.get("/health", tags=["ops"])
    def health() -> dict[str, str]:
        return {"status": "ok", "version": settings.app_version, "env": settings.app_env}

    Instrumentator().instrument(app).expose(app, endpoint="/metrics", tags=["ops"])
    return app


app = create_app()
