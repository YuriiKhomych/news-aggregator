#!/bin/sh

# wait for PSQL server to start
sleep 10

su -m myuser -c "python manage.py makemigrations news"
# migrate db, so we have the latest db schema
su -m myuser -c "python manage.py migrate"
# load feed data
su -m myuser -c "python manage.py loaddata feed.json"
# start development server on public ip interface, on port 8000
su -m myuser -c "python manage.py runserver 0.0.0.0:8000"