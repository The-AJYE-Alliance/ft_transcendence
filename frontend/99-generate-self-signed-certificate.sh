#!/bin/sh
set -e

if [ ! -e "/etc/ssl/${HOSTNAME}.key" ]; then
  echo "SSL key for ${HOSTNAME} not found. Generating a new self-signed SSL certificate..."
  openssl req -x509 -newkey rsa:4096 -nodes -out /etc/ssl/${HOSTNAME}.crt \
    -keyout /etc/ssl/${HOSTNAME}.key -days 365 \
    -subj "/C=FR/O=Ecole 42/OU=42.fr/CN=${HOSTNAME}"
  echo "SSL certificate generated and saved at /etc/ssl/${HOSTNAME}.crt"
  chmod 644 /etc/ssl/${HOSTNAME}.key /etc/ssl/${HOSTNAME}.crt
  echo "Permissions set for SSL key and certificate."
else
  echo "SSL key for ${HOSTNAME} already exists. Skipping certificate generation."
fi