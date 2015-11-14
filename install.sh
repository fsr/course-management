#!/usr/bin/env bash
set -e

# change to project root directory

# install project dependencies
python3 -m pip install -r requirements.txt

# download and install static files
curl -L https://github.com/twbs/bootstrap/releases/download/v3.3.5/bootstrap-3.3.5-dist.zip -o bootstrap.zip
curl code.jquery.com/jquery-1.11.3.min.js -o jquery.min.js

unzip bootstrap.zip

rsync -av bootstrap-3.3.5-dist/ src/static/vendor/
mv jquery.min.js src/static/vendor/js

rm bootstrap.zip
rm -r bootstrap-3.3.5-dist
