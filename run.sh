#!/usr/bin/env bash
# Run Django app using Gunicorn
gunicorn travel_agent_project.wsgi:application --bind 0.0.0.0:$PORT
