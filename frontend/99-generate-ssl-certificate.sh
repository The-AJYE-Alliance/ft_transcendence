#!/bin/sh

set -e

if [ -f "/etc/ssl/${HOSTNAME}" ] && openssl x509 -checkend 86400 -noout -in /etc/ssl/"${HOSTNAME}"; then
  echo "Certificate is present and valid"
  return
fi

echo "Certificate expired or missing, generating new certificate..."
RESULT=$(curl --cacert /ca/ca.pem --header "X-Vault-Token: $VAULT_TOKEN" \
  --request POST \
  --data "{'common_name': \"${HOSTNAME}\", 'ttl': '876000h'}" \
  "$VAULT_ADDR"/v1/pki_int/issue/nginx)

echo "$RESULT" | jq -r .data.certificate | tee /etc/ssl/"${HOSTNAME}".crt
echo "$RESULT" | jq -r .data.private_key | tee /etc/ssl/"${HOSTNAME}".key