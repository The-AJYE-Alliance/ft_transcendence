#!/bin/sh

RESULT=$(curl --header "X-Vault-Token: $VAULT_TOKEN" \
  --request POST \
  --data "{'common_name': \"${HOSTNAME}\", 'ttl': '876000h'}" \
  "$VAULT_ADDR"/v1/pki_int/issue/nginx)

echo "$RESULT" | jq -r .data.certificate | tee /etc/ssl/"${HOSTNAME}".crt
echo "$RESULT" | jq -r .data.private_key | tee /etc/ssl/"${HOSTNAME}".key