CSS_DIR = static/css
JS_DIR = static/vendor/js
PYTHON_ENV_FOLDER = env

ifeq ($(OS), Windows_NT)
PYTHON = $(PYTHON_ENV_FOLDER)/Scripts/python3.exe
else
PYTHON = $(PYTHON_ENV_FOLDER)/bin/python
endif


js_files = jquery/dist/jquery.min.js jquery-ui/jquery-ui.min.js foundation/js/foundation.min.js fastclick/lib/fastclick.js modernizr/modernizr.js jquery/dist/jquery.min.map

all: pip sass

sass: bower submodule
	sass -I corporate-web-design/src -I bower_components/foundation/scss sass/style.sass $(CSS_DIR)/style.css

submodule:
	git submodule init
	git submodule update

bower: 
	bower install
	cp $(addprefix bower_components/, $(js_files)) $(JS_DIR)

ifdef $(NO_VIRTUALENV)
pip: 
else
pip: virtualenv
endif
	$(PYTHON) -m pip install -r requirements.txt

virtualenv:
	python3 -m pip install virtualenv
	python3 -m virtualenv $(PYTHON_ENV_FOLDER)

clean:
	rm -r bower_components $(CSS_DIR)/* $(JS_DIR)/*

migrate: pip
ifeq ($(wildcard db.sqlite3),)
	$(PYTHON) manage.py makemigrations
	$(PYTHON) manage.py migrate
	$(PYTHON) manage.py loaddata courses
endif
