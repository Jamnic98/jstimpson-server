from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.routers.activities_router import router as activities_router
from app.core.routers.runs_router import router as runs_router
from app.utils.config import settings


def create_fastapi_app():
    app = FastAPI(debug=settings.DEBUG)

    # add middleware
    # noinspection PyTypeChecker
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost",
            "http://localhost:8080"
        ],
        allow_methods=["GET"],
        allow_headers=["*"]
    )

    # add health check endpoint
    @app.get("/health")
    def health_check():
        return JSONResponse({"status": "ok"}, 200)

    # add routers
    app.include_router(activities_router)
    app.include_router(runs_router)

    return app
