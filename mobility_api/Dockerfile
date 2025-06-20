FROM python:3.13-alpine

RUN apk add --update gcc g++ linux-headers curl

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY * /app
WORKDIR /app
ENTRYPOINT [ "uvicorn", "main:app" ]
