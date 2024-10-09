FROM hashicorp/vault:1.17

RUN apk add --no-cache openssl

COPY scripts/pre-init.sh /pre-init.sh
COPY config.hcl /vault/config/config.hcl
ENTRYPOINT ["/pre-init.sh"]