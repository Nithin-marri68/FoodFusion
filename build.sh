#!/usr/bin/env bash

set -o errexit

cd "Food Ordering/foodOrderSystem"

python manage.py collectstatic --no-input

python manage.py migrate