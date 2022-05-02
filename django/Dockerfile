# syntax=docker/dockerfile:1

FROM python:3.10.0-alpine
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./clustering/src/* ./clustering/
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev build-base
RUN pip install --upgrade pip
RUN pip install pipenv pybind11
COPY ./django/Pipfile* ./
RUN pipenv install
COPY ./django/ ./
# -lstdc++ did not help, 20->17 didn't help
RUN gcc -O2 -Wall -shared -std=c++17 -lstdc++ -fPIC $(python -m pybind11 --includes) ./clustering/*.cpp -o data/stores/clustering.so
# temp dev server
CMD pipenv run python manage.py migrate && pipenv run python manage.py runserver 0.0.0.0:8001
