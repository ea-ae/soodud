# syntax=docker/dockerfile:1

# FROM python:3.10.0-alpine
FROM python:3.10.0
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# COPY ./clustering/src/* ./clustering/
# RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev libc-dev gpgme-dev build-base
RUN apt-get update && apt-get install --yes gcc python3-dev musl-dev build-essential
RUN pip install --upgrade pip
RUN pip install pipenv pybind11
COPY . ./
RUN pipenv install --system --deploy --ignore-pipfile

RUN g++ -O2 -Wall -shared -std=c++20 -lstdc++ --verbose -fPIC $(python -m pybind11 --includes) \
./clustering/src/*.cpp -o data/stores/clustering.so

# temp dev server
RUN python manage.py collectstatic --noinput
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8001
