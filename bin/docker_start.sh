#!/usr/bin/env bash
NAME="maple"
DJANGODIR=/code/maple
USER=root
GROUP=root
NUM_WORKERS=1
DJANGO_WSGI_MODULE=maple.wsgi


echo "Starting $NAME as `whoami`"

cd $DJANGODIR

export PYTHONPATH=$DJANGODIR:$PYTHONPATH

python manage.py makemigrations && \
  python manage.py migrate && \
  python manage.py collectstatic --noinput  && \
  python manage.py compress --force && \
  python manage.py build_index && \
  python manage.py compilemessages

exec gunicorn ${DJANGO_WSGI_MODULE}:application \
--name $NAME \
--workers $NUM_WORKERS \
--user=$USER --group=$GROUP \
--bind 0.0.0.0:8000 \
--log-level=debug \
--log-file=- \
--worker-class gevent \
--threads 4
