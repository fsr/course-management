#!/usr/bin/env bash

set -e

cd src

rm db.sqlite3
python3 manage.py migrate
python3 manage.py loaddata courses