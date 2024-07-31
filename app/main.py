from uvicorn import run

from app.factories.fastapi_app import create_fastapi_app

app = create_fastapi_app()


if __name__ == "__main__":
    run("app.main:app", port=8080, reload=True)
