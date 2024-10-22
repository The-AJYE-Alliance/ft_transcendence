# syntax=docker/dockerfile:1

FROM nginx:1.27.1

RUN apt-get update && apt-get install -y --no-install-recommends jq

COPY 99-generate-ssl-certificate.sh /docker-entrypoint.d
COPY default.conf.template /etc/nginx/templates/default.conf.template

CMD [ "nginx", "-g", "daemon off;" ]