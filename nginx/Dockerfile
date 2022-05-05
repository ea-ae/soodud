# syntax=docker/dockerfile:1

FROM nginx:1.21 as base
WORKDIR /static
# VOLUME /static
EXPOSE 80

RUN apt-get update && apt-get install --yes fail2ban
COPY fail2ban/jail.local /etc/fail2ban/jail.local
COPY fail2ban/filter.d/* /etc/fail2ban/filter.d/
RUN service fail2ban restart
COPY *.conf /etc/nginx/

# CMD /bin/bash \
#     envsubst < /etc/nginx/conf.d/nginx.template.conf > /etc/nginx/nginx.conf && \
#     envsubst < /etc/nginx/conf.d/ssl*.template.conf > /etc/nginx/nginx.conf && \
#     nginx -g 'daemon off;'
