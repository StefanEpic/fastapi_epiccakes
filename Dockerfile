FROM python:3.10-alpine

COPY requirements.txt .

RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN apk del .tmp-build-deps

COPY . .

WORKDIR src

CMD gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --forwarded-allow-ips='*' --bind=0.0.0.0:8000