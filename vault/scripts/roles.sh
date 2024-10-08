#!/bin/sh

set -e

ROLE_INIT_FILE=/vault/secrets/role.init

if [ ! -f ${ROLE_INIT_FILE} ]; then
  echo "Enabling AppRole Auth Backend..."
  vault auth enable approle
  touch "${ROLE_INIT_FILE}"
fi

APP_INIT_FILE=/vault/secrets/${APP}.init
if [ -f "${APP_INIT_FILE}" ]; then
  echo "${APP_INIT_FILE} exists. Vault already initialized for ${APP}."
else
  echo "Enabling Secrets Engine for ${APP}..."
  vault secrets enable -path="${APP}-kv" kv-v2

  echo "Creating ${APP} Policy..."
  vault policy write "${APP}" /vault/policies/"${APP}".hcl

  echo "Creating ${APP} Approle Auth Backend..."
  vault write auth/approle/role/"${APP}" token_policies="${APP}" token_tll=2h token_max_ttl=6h

  echo "${APP} Approle creation complete."
  touch "${APP_INIT_FILE}"
fi