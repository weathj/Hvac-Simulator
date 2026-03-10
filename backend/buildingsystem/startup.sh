#!/bin/bash

set -eu

python manage.py makemigrations
python manage.py migrate
python manage.py loaddata hvac_data
uvicorn server.asgi:application --host 0.0.0.0 --port 8000
