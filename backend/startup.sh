#!/bin/bash

set -eu

python manage.py migrate
python manage.py loaddata hvac_data
gunicorn --bind 0.0.0.0:8000 server.wsgi
