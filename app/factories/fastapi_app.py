from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from app.factories.scheduler import create_scheduler
from app.factories.database import mongo_client
from app.core.routers.activities_router import router as activities_router
from app.core.routers.runs_router import router as runs_router
from app.utils.config import settings


@asynccontextmanager
async def __lifespan(_app: FastAPI):
    # schedule tasks
    # create_scheduler().start()
    yield
    # close connections
    mongo_client.close()


def create_fastapi_app():
    app = FastAPI(lifespan=__lifespan, debug=settings.DEBUG)

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
        return {"status": "ok"}

    # add routers
    app.include_router(activities_router)
    app.include_router(runs_router)
    return app
