#!/usr/bin/env bash
set -eux
./wait-for-it.sh --host=$POSTGRES_HOST --port=$POSTGRES_PORT
./manage.py migrate
./manage.py createsuperuser --no-input --email master@localhost.localdomain
./manage.py runserver 0:8000