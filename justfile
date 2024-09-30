DOCKER := 'docker compose'
APP_1 := "auth"
APP_2 := "pong"
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
	@echo "{{GREEN}}██████████████████████ Running Containers ██████████████████████{{RESET}}"
	@{{DOCKER}} up -d
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
	{{DOCKER}} down

shell c="":
    {{DOCKER}} exec -it {{c}} sh

migrations:
    @echo "{{BLUE}}██████████████████████ Making Migrations ██████████████████████{{RESET}}"
    {{DOCKER}} exec {{APP_1}} python manage.py makemigrations
    {{DOCKER}} exec {{APP_2}} python manage.py makemigrations

_env:
    #!/bin/bash
    set -euo pipefail
    if test ! -e .env; then
      echo -e "{{YELLOW}}Copying .env files...{{RESET}}\n"
      cp .env.example .env
      cp auth.env.example auth.env
      cp pong.env.example pong.env
    fi

reload: down build up