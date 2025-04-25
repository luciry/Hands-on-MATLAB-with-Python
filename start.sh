#!/bin/bash
# start.sh
echo "Starting application"
gunicorn wsgi:app 