#!/bin/sh
set -e

echo "Starting Django..."

echo "Applying database migrations..."
python manage.py migrate --noinput
echo "Database migrations completed."

echo "Collecting static files..."
python manage.py collectstatic --noinput
echo "Static files collected."

exec "$@"