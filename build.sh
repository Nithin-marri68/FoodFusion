#!/usr/bin/env bash

set -o errexit

python -m pip install --upgrade pip
python -m pip install -r "Food Ordering/requirements.txt"

cd "Food Ordering/foodOrderSystem"

python manage.py collectstatic --no-input

python manage.py migrate