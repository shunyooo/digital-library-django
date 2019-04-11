#!/bin/sh

# Collect static files
echo "#### Collect static files"
./manage.py collectstatic --noinput

# Apply database migrations
echo "#### Apply database migrations"
./manage.py migrate

echo "#### Starting Jupyter Notebook"
./manage.py shell_plus --notebook &

echo "#### Starting Celery"
celery -A library worker -l info &

# Start server
echo "#### Starting server"
./manage.py runserver 0.0.0.0:8000