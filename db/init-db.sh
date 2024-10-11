#!/bin/bash

set -e

psql -v ON_ERROR_STOP=1 --username postgres <<-EOSQL
  CREATE USER vaultadmin WITH LOGIN PASSWORD 'tobechanged' CREATEROLE;
	CREATE ROLE owner WITH NOINHERIT;
	CREATE DATABASE $DB_NAME OWNER owner;
	GRANT owner TO vaultadmin WITH ADMIN OPTION;
EOSQL