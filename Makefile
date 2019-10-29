PYTHON_ENV_FOLDER = env
SASS = sassc

ifeq ($(OS), Windows_NT)
PYTHON = $(PYTHON_ENV_FOLDER)/Scripts/python3.exe
else
PYTHON = $(PYTHON_ENV_FOLDER)/bin/python
endif

css_files = static/css/style.css

all: pip $(css_files)

static/css/%.css: sass/%.sass
	if [ ! -d "./static/css" ] ; then  mkdir -p static/css; fi
	$(SASS) -m -I corporate-web-design/src -I sass/vendor "$<" "$@"

submodule:
	git submodule init
	git submodule update

ifdef $(NO_VIRTUALENV)
pip: 
else
pip: virtualenv
endif
	$(PYTHON) -m pip install -r requirements.txt

virtualenv:
ifeq ($(wildcard $(PYTHON)),)
	python3 -m pip install virtualenv
	python3 -m virtualenv $(PYTHON_ENV_FOLDER)
endif

clean:
	rm -r bower_components $(CSS_DIR)/style.css $(JS_DIR)/*

migrate: pip
ifeq ($(wildcard db.sqlite3),)
	$(PYTHON) manage.py makemigrations
	$(PYTHON) manage.py migrate
	$(PYTHON) manage.py loaddata courses
endif
