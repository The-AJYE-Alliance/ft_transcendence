DOCKER := 'docker --log-level ERROR compose'
APPS := "nginx"
RED := '\033[1;31m'
GREEN := '\033[1;32m'
YELLOW := '\033[1;33m'
BLUE := '\033[1;34m'
RESET := '\033[0m'

default: build up

ls:
	@echo "{{GREEN}}██████████████████████████ IMAGES ███████████████████████████{{RESET}}"
	@docker images
	@echo "{{YELLOW}}██████████████████████ ALL CONTAINERS ███████████████████████{{RESET}}"
	@docker ps -a

build: _env
	@echo "{{BLUE}}██████████████████████ Building Images ███████████████████████{{RESET}}"
	{{DOCKER}} build

up: _env
    #!/usr/bin/env bash
    @echo "{{GREEN}}██████████████████████ Running Containers ██████████████████████{{RESET}}"
    docker --log-level ERROR compose up -d vault vault-init
    while [ "$(docker --log-level ERROR compose exec vault-init "echo "Waiting..." 2>&1 /dev/null")" ]; do
      true
    done
    . "./vault/scripts/launch.sh" {{APPS}}
    @echo "{{RED}}╔════════════════════════════║NOTE:║════════════════════════╗{{RESET}}"
    @echo "{{RED}}║   {{BLUE}} You can see The Containers logs using {{YELLOW}}just logs        {{RED}}║{{RESET}}"
    @echo "{{RED}}╚═══════════════════════════════════════════════════════════╝{{RESET}}"

logs:
	@echo "{{GREEN}}██████████████████████ Running Containers ██████████████████████{{RESET}}"
	@{{DOCKER}} logs

status:
	@echo "{{GREEN}}██████████████████████ The Running Containers ██████████████████████{{RESET}}"
	@docker ps

stop:
	@echo "{{RED}}████████████████████ Stopping Containers █████████████████████{{RESET}}"
	{{DOCKER}} stop

start:
	@echo "{{RED}}████████████████████ Starting Containers █████████████████████{{RESET}}"
	{{DOCKER}} start

down:
	@echo "{{RED}}██████████████████ Removing All Containers ██████████████████{{RESET}}"
	{{DOCKER}} down --remove-orphans -v

watch: build
    @echo "{{GREEN}}██████████████████████ Watching Containers... ██████████████████████{{RESET}}"
    {{DOCKER}} up --watch

shell c="":
    {{DOCKER}} exec -it {{c}} sh

migrations:
    @echo "{{BLUE}}██████████████████████ Making Migrations ██████████████████████{{RESET}}"
    python ./backend/auth/manage.py makemigrations
    python ./backend/pong/manage.py makemigrations

_env:
    #!/usr/bin/env bash
    set -euo pipefail
    if test ! -e .env; then
      echo -e "{{YELLOW}}Copying .env files...{{RESET}}\n"
      cp .env.example .env
      cp auth.env.example auth.env
      cp pong.env.example pong.env
    fi

reload: down build up