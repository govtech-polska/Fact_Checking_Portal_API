#!/bin/sh
uwsgi --http 0.0.0.0:8000 --wsgi-file sfnf_portal/wsgi.py
exec "$@"
