import os
import uvicorn

from app.utils.logger import logger
from app.factories.fastapi import create_fastapi_app


app = create_fastapi_app()
logger.info("FastAPI app created.")

PORT = os.getenv('PORT', 8080)
uvicorn.run(app, host="127.0.0.1", port=PORT, log_level="debug")
