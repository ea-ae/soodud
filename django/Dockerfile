# syntax=docker/dockerfile:1

FROM python:3.10.0-alpine
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --upgrade pip
RUN pip install pipenv
COPY Pipfile* ./
RUN pipenv install
COPY . ./
# temp dev server
CMD pipenv run python manage.py migrate && pipenv run python manage.py runserver 0.0.0.0:8001
