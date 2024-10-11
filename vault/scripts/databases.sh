#!/bin/bash

set -e

export VAULT_CACERT=/vault/ssl/cert.pem
VAULT_TOKEN="$(cat /vault/secrets/token)"
export VAULT_TOKEN
DB_INIT_FILE=/vault/secrets/database.init
APP=$1

if [ ! -f ${DB_INIT_FILE} ]; then
  echo "Enabling Database Backend..."
  vault secrets enable database
  touch "${DB_INIT_FILE}"
fi

APPDB_INIT_FILE=/vault/secrets/${APP}-db.init
if [ -f "${APPDB_INIT_FILE}" ]; then
  echo "${APPDB_INIT_FILE} exists. Database already initialized for ${APP}."
else
  echo "Enabling Database Engine for ${APP}..."
  vault write database/config/"${APP}" \
     plugin_name=postgresql-database-plugin \
     connection_url="postgresql://{{username}}:{{password}}@${APP}-db:5432/${APP}?sslmode=disable" \
     allowed_roles="${APP}" \
     username="vaultadmin" \
     password="tobechanged"

  echo "Rotating the root password..."
  vault write -force database/rotate-root/"${APP}"

  echo "Creating ${APP} Database Role..."
  vault write database/roles/"${APP}" \
      db_name="${APP}" \
      creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}' IN ROLE \"owner\" INHERIT NOCREATEROLE NOCREATEDB NOSUPERUSER NOREPLICATION NOBYPASSRLS;" \
      revocation_statements="DROP ROLE \"{{name}}\";" \
      default_ttl=1h \
      max_ttl=24h

  echo "${APP} Database creation complete."
  touch "${APPDB_INIT_FILE}"
fi