from uvicorn import run
from mangum import Mangum

from app.factories.fastapi_app import create_fastapi_app
from app.config import settings

app = create_fastapi_app()
handler = Mangum(app)

if __name__ == "__main__":
    log_level = "warning"  # Default log level for Uvicorn
    if settings.DEBUG:
        log_level = "debug"
    run("main:app", port=8080, log_level=log_level, reload=settings.RELOAD)
