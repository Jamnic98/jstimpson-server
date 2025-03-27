from uvicorn import run
from mangum import Mangum

from app.factories.fastapi_app import create_fastapi_app
from app.utils.config import settings

app = create_fastapi_app()
handler = Mangum(app)


if __name__ == "__main__":
    LOG_LEVEL = "warning"
    if settings.DEBUG:
        LOG_LEVEL = "debug"

    run("main:app", port=8080, log_level=LOG_LEVEL, reload=settings.RELOAD)
