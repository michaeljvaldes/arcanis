#!/bin/sh


# echo "Flushing database"
# python manage.py flush --no-input

echo "Migrating database"
python manage.py migrate

# echo "Loading fixtures"
# python manage.py loaddata some_users commanders squirrels

exec gunicorn arcanis.wsgi:application --bind 0.0.0.0:8000