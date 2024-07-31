FROM python:3.10

COPY . .

RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 8080

ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
