from mangum import Mangum

from app.factories.fastapi import create_fastapi_app


app = create_fastapi_app()
handler = Mangum(app)
