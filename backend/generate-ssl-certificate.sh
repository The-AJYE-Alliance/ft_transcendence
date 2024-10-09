#!/bin/sh

set -e

HOSTNAME=${APP_NAME}.api.${HOSTNAME}

if [ -f "/etc/ssl/${HOSTNAME}.crt" ] && openssl x509 -checkend 86400 -noout -in /etc/ssl/"${HOSTNAME}.crt"; then
  echo "Certificate is present and valid"
  return
fi

APP_TOKEN=$(curl --cacert /ca/ca.pem -s --request POST --data "{\"role_id\": \"${APP_RID}\", \"secret_id\": \"${APP_SID}\"}" "$VAULT_ADDR"/v1/auth/approle/login | jq -r .auth.client_token)

echo "Certificate expired or missing, generating new certificate..."
RESULT=$(curl --cacert /ca/ca.pem -s --header "X-Vault-Token: $APP_TOKEN" \
  --request POST \
  --data "{\"common_name\":\"${HOSTNAME}\",\"ttl\":\"450h\"}" \
  "$VAULT_ADDR/v1/pki_int/issue/domain")

echo "$RESULT" | sed 's/$/\\n/' | tr -d '\n' | sed -e 's/“/"/g' -e 's/”/"/g' | sed '$ s/\\n$//' | jq -r .data.certificate | tee /etc/ssl/"${HOSTNAME}".crt
echo "$RESULT" | sed 's/$/\\n/' | tr -d '\n' | sed -e 's/“/"/g' -e 's/”/"/g' | sed '$ s/\\n$//' | jq -r .data.private_key | tee /etc/ssl/"${HOSTNAME}".key