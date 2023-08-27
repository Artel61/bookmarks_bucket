FROM python:3.10

ENV PYTHONBUFFERED 1

WORKDIR /app

COPY bookmarks_bucket /app
COPY .service.env /app/.env
COPY deploy.sh /app/deploy.sh
COPY requirements.txt /app/requirements.txt
RUN chmod +x /app/deploy.sh


RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt
