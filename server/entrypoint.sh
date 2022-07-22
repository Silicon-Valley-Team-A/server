#!bin/bash
python3 manage.py makemigrations account

python3 manage.py makemigrations playlist

python3 manage.py makemigrations model

python3 manage.py migrate

gunicorn --bind 0.0.0.0:8000 server.wsgi:application -t 240