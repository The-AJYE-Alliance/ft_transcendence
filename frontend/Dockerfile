# syntax=docker/dockerfile:1

FROM nginx:1.27.1

COPY 99-generate-self-signed-certificate.sh /docker-entrypoint.d
COPY default.conf.template /etc/nginx/templates/default.conf.template
COPY static /usr/share/nginx/html

CMD [ "nginx", "-g", "daemon off;" ]