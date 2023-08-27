#!/bin/bash

python manage.py migrate

python manage.py createsuperuser --username "$DJ_SUPERUSER" --email some@email.se

python manage.py add_default_link_types
