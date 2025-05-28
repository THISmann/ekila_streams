#!/bin/sh

# checks if a PostgreSQL database named "ekila_db" exists otherwise create it.
# by performing extraction from databases in a quiet, tabular format.
cp ekila_streams/settings_docker_example.py ekila_streams/settings_docker.py

while ! PGPASSWORD=8Fny?aXEFkh9ePA3 psql -h ${POSTGRES_HOST} -U postgres -c '\q'; do echo "En attente du demarrage de postgresql..." && sleep 1; done
echo "BD demarré avec succès.......>>"
if ! PGPASSWORD=8Fny?aXEFkh9ePA3 psql -U postgres -h ${POSTGRES_HOST} -p ${POSTGRES_PORT} -lqt | cut -d \| -f 1 | cut -d ' ' -f 2 | grep -q "^ekila_db$"; then
    PGPASSWORD=8Fny?aXEFkh9ePA3 createdb -U postgres -h ${POSTGRES_HOST} -p ${POSTGRES_PORT} ekila_db
else
    echo "La database existe déjà..."
fi

mkdir -p ${DJANGO_STATIC_ROOT} && chown ekiladm:www-data ${DJANGO_STATIC_ROOT}
mkdir -p ${DJANGO_MEDIA_ROOT} && chown ekiladm:www-data ${DJANGO_MEDIA_ROOT}
mkdir -p ${POSTGRES_DATA} && chown ekiladm:www-data ${POSTGRES_DATA}

#django wait for db before migrating
gosu ekiladm make wait_db
gosu ekiladm make migrate
gosu ekiladm make collectstatic

echo "Server starting at port ${DJANGO_DEV_SERVER_PORT}....."
USER_EXISTS="from django.contrib.auth import get_user_model; User = get_user_model(); exit(User.objects.exists())"
python manage.py shell -c "$USER_EXISTS" && python manage.py createsuperuser --noinput
exec gosu ekiladm daphne -b 0.0.0.0 -p ${DJANGO_DEV_SERVER_PORT} ekila_streams.asgi:application
#exec gosu ekiladm uwsgi --http-socket :${DJANGO_DEV_SERVER_PORT} --uid ekiladm --ini config_files/basic-docker.ini --processes 4 --threads 2 --wsgi-file ekila_streams/wsgi.py
