# syntax=docker/dockerfile:1

# FROM python:3.10.0-alpine
FROM python:3.10.0
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install --yes gcc python3-dev musl-dev build-essential
RUN pip install --upgrade pip
RUN pip install pipenv pybind11
COPY . ./
RUN pipenv install --system --deploy --ignore-pipfile

RUN g++ -O2 -Wall -shared -std=c++20 -lstdc++ --verbose -fPIC $(python -m pybind11 --includes) \
./clustering/src/*.cpp -o data/stores/clustering.so

CMD python manage.py collectstatic --noinput && \
# python manage.py createsuperuser --noinput && \  # error if user already exists, can't put it above bc no .env
python manage.py migrate && \
python manage.py shell -c "import soodud.services as s; s.load_cache()" && \
gunicorn -b 0.0.0.0:8001 -w 3 --timeout 70 soodud.wsgi
