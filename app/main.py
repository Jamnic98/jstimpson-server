from typing import Any
from mangum import Mangum

from app.utils.logger import logger
from app.factories.fastapi import create_fastapi_app


app = create_fastapi_app()
logger.info("FastAPI app created.")

def handler(event: dict, _context=None) -> Any:
    asgi_handler = Mangum(app)
    return asgi_handler(event, _context)


if __name__ == "__main__":
    import os
    import uvicorn

    os.environ["AWS_SAM_LOCAL"] = "TRUE"
    os.environ["LOG_LEVEL"] = "DEBUG"
    uvicorn.run(
        "app.main:app", port=8080, log_level="debug", reload=True, access_log=False
    )
