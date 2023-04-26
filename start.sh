#!/bin/bash

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn CarShipping.wsgi:application \
    python manage.py runserver \
    --bind 0.0.0.0:8000 \
    --workers 3
