# syntax=docker/dockerfile:1

FROM node:17.4-alpine3.15
EXPOSE 9001
ENV PATH /app/node_modules/.bin:$PATH

WORKDIR /app
VOLUME /app/dist
COPY package*.json ./
RUN npm ci
COPY . ./
CMD npm run prod
