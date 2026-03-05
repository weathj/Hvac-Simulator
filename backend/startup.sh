#!/bin/bash

set -eu

gunicorn --bind 0.0.0.0:8000 server.wsgi &
python manage.py run-simulation
