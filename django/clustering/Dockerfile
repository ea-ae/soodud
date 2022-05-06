# syntax=docker/dockerfile:1

FROM gcc:11

WORKDIR /app
COPY src/ ./

CMD gcc src/*.cpp -o out/clustering.so -shared -fPIC -std=c++20 -O2 -Wall
