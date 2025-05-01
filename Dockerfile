FROM python:3.12-alpine

WORKDIR /app

COPY /app ./app
COPY /main.py ./
COPY /requirements.txt ./
COPY /.env.local ./

RUN pip install -r requirements.txt

#--no-cache-dir

EXPOSE 8080

CMD ["python3", "-m", "main"]
