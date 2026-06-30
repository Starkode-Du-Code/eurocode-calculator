"""Point d'entrée FastAPI."""

import uvicorn
from fastapi import FastAPI

from eurocode_calculator import __version__
from eurocode_calculator.config import settings
from eurocode_calculator.routers import beam_router, column_router, foundation_router


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=__version__,
        description=(
            "API REST de vérification structurelle selon les Eurocodes. "
            "Remplace les feuilles Excel de calcul par des endpoints testables et déployables."
        ),
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.include_router(beam_router)
    app.include_router(column_router)
    app.include_router(foundation_router)

    @app.get("/health", tags=["Système"])
    def health():
        return {"status": "ok", "version": __version__}

    @app.get("/", tags=["Système"])
    def root():
        return {
            "message": "Eurocode Calculator API",
            "docs": "/docs",
            "endpoints": {
                "beam_uls": "POST /beam/verify-uls",
                "beam_shear": "POST /beam/verify-shear",
                "beam_uls_capacity": "POST /beam/verify-uls-capacity",
                "column_buckling": "POST /column/buckling",
                "foundation_bearing": "POST /foundation/bearing",
            },
        }

    return app


app = create_app()


def run() -> None:
    uvicorn.run(
        "eurocode_calculator.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )


if __name__ == "__main__":
    run()
