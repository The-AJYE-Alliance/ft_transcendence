#!/bin/sh
set -e

if [ ! -e "/etc/ssl/${NGINX_HOST}.key" ]; then
  echo "SSL key for ${NGINX_HOST} not found. Generating a new self-signed SSL certificate..."
  openssl req -x509 -newkey rsa:4096 -nodes -out /etc/ssl/${NGINX_HOST}.crt \
    -keyout /etc/ssl/${NGINX_HOST}.key -days 365 \
    -subj "/C=FR/O=Ecole 42/OU=42.fr/CN=${NGINX_HOST}"
  echo "SSL certificate generated and saved at /etc/ssl/${NGINX_HOST}.crt"
  chmod 644 /etc/ssl/${NGINX_HOST}.key /etc/ssl/${NGINX_HOST}.crt
  echo "Permissions set for SSL key and certificate."
else
  echo "SSL key for ${NGINX_HOST} already exists. Skipping certificate generation."
fi