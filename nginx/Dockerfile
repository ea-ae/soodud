# syntax=docker/dockerfile:1

FROM nginx:1.21 as base
WORKDIR /etc/nginx/
EXPOSE 80

RUN apt-get update && apt-get install --yes iptables fail2ban
COPY fail2ban/*.local /etc/fail2ban/
COPY fail2ban/filter.d/* /etc/fail2ban/filter.d/
# remove symlink nginx log files and replace them so that fail2ban can read them
RUN find /var/log/nginx/* -maxdepth 1 -type l -delete
# RUN rm /var/log/nginx/*.log
RUN touch /var/log/nginx/access.log
RUN touch /var/log/nginx/error.log
COPY *.conf .

# fail2ban depends on nginx, tail routes non-symlink access.log back into stdout
CMD nginx & rm -f /var/run/fail2ban/fail2ban.sock && tail -n0 -f /var/log/fail2ban.log & \
service fail2ban start && tail -n0 -f /var/log/nginx/access.log

# CMD /bin/bash \
#     envsubst < /etc/nginx/conf.d/nginx.template.conf > /etc/nginx/nginx.conf && \
#     envsubst < /etc/nginx/conf.d/ssl*.template.conf > /etc/nginx/nginx.conf && \
#     nginx -g 'daemon off;'
