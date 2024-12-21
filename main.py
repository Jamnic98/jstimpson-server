from uvicorn import run
from mangum import Mangum

from app.factories.fastapi_app import create_fastapi_app

app = create_fastapi_app()
handler = Mangum(app)

if __name__ == "__main__":
    run("main:app", port=8080, reload=True)
