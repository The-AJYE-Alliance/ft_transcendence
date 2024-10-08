#!/bin/sh

set -e

export VAULT_CACERT=/vault/ssl/cert.pem
VAULT_TOKEN="$(cat /vault/secrets/token)"
export VAULT_TOKEN

if [ "${2}" = "rid" ]; then
  RESULT=$(vault read auth/approle/role/"${1}"/role-id | grep 'role_id' | awk '{print $2}')
else
  RESULT=$(vault write -force auth/approle/role/"${1}"/secret-id | grep 'secret_id' | awk '{print $2}' | head -n 1)
fi

echo "${RESULT}"