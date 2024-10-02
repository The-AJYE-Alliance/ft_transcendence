#!/usr/bin/dumb-init /bin/sh

set -e

if [ ! -f /vault/ssl/key.pem ] || [ ! -f /vault/ssl/cert.pem ]; then
  echo "SSL certificate missing, generating..."
  openssl req -x509 -newkey rsa:4096 -nodes -out /vault/ssl/cert.pem \
    -keyout /vault/ssl/key.pem -days 365 -subj "/C=FR/O=Ecole 42/OU=42.fr/CN=vault" \
    -addext "subjectAltName=DNS:vault"
  chmod 644 /vault/ssl/cert.pem /vault/ssl/key.pem
fi

. "docker-entrypoint.sh" "$@"