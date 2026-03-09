#!/bin/bash

set -eu

python manage.py loaddata hvac_data
python manage.py migrate
gunicorn --bind 0.0.0.0:8000 server.wsgi
