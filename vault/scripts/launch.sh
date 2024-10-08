#!/usr/bin/env bash

ENVS=()

decl_secrets () {
  local APP=$1
  ENVS+=( "${APP^^}"_RID="$(docker --log-level ERROR compose run --rm vault-init "sh" "-c" "/vault/scripts/get-secret.sh ${APP} rid")" )
  ENVS+=( "${APP^^}"_SID="$(docker --log-level ERROR compose run --rm vault-init "sh" "-c" "/vault/scripts/get-secret.sh ${APP} sid")" )
}


IFS=' ' read -r -a apps <<< "$1"

for app in "${apps[@]}"; do
  decl_secrets "$app"
done

env "${ENVS[@]}" docker compose up -d