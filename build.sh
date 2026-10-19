#!/usr/bin/env bash
# Render build script: install dependencies, collect static files, migrate.
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate --no-input
python manage.py createcachetable
