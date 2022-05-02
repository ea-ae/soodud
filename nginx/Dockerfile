# syntax=docker/dockerfile:1

FROM nginx:1.21 as base
WORKDIR /static
# VOLUME /static
EXPOSE 80
COPY *.conf /etc/nginx/
# CMD /bin/bash \
#     envsubst < /etc/nginx/conf.d/nginx.template.conf > /etc/nginx/nginx.conf && \
#     envsubst < /etc/nginx/conf.d/ssl*.template.conf > /etc/nginx/nginx.conf && \
#     nginx -g 'daemon off;'
