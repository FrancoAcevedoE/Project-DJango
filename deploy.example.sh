#!/bin/bash
# -*- ENCODING: UTF-8 -*-/
export DATABASES_ENGINE='django.db.backends.postgresql_psycopg2'
export DATABASES_NAME='dbname'
export DATABASES_USER='dbuser'
export DATABASES_PASSWORD='dbpassword'
export DATABASES_HOST='localhost'
export DATABASES_PORT=''
export EMAIL_HOST_USER='username@domain.com'
export EMAIL_HOST_PASSWORD='123456'

echo ">> Django Congress staging"
# shellcheck disable=SC2164
cd /var/www/django-congress/

echo ">> Pull repository"
git status
git pull

echo ">> Activar venv"
. venv/bin/activate

echo ">> Install requirements"
pip install -r requirements.txt

echo ">> Import staticfiles"
python manage.py collectstatic --no-input --clear

echo ">> Migrate"
python manage.py migrate

# python manage.py createsuperuser
# python manage.py loaddata admin_interface_theme_bootstrap.json
# python manage.py loaddata admin_interface_theme_foundation.json
# python manage.py loaddata admin_interface_theme_uswds.json

echo ">> Deactivate venv "
deactivate

echo ">> Restart apache"
systemctl restart apache2

echo ">> Finish..."

exit