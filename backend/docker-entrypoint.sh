#!/bin/sh
set -e

echo "Starting Django..."

echo "Applying database migrations..."
python manage.py migrate --noinput
echo "Database migrations completed."

exec "$@"