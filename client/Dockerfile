# syntax=docker/dockerfile:1

# Common
FROM node:17.4-alpine3.15 AS base
EXPOSE 9001
ENV PATH /app/node_modules/.bin:$PATH

WORKDIR /app
VOLUME /app/dist
COPY package*.json ./
RUN npm ci
COPY . ./
CMD npm run prod
