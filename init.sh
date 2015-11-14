#!/usr/bin/env bash

set -e

cd src

python3 manage.py migrate
python3 manage.py loaddata courses