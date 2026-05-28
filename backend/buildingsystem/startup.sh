#!/bin/bash

set -eu

RELOAD_FLAG=""

if [ "${DJANGO_DEV:-false}" = "true" ]; then
    RELOAD_FLAG="--reload"
fi

python manage.py makemigrations
python manage.py migrate
python manage.py loaddata hvac_data

uvicorn server.asgi:application --host 0.0.0.0 --port 8000 $RELOAD_FLAG