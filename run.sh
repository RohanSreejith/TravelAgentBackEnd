#!/usr/bin/env bash
# Exit on error
set -o errexit

python manage.py migrate --noinput
gunicorn travel_agent_project.wsgi:application --bind 0.0.0.0:$PORT
