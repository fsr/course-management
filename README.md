# The real course-management

## Gettin' started

### Required software

* Python 3
* nodejs and npm
* Ruby and Sass 


### Installation

* install dependencies

  ```
  $ npm install -g bower
  $ sudo gem install sass --no-user-install
  $ make
  ```

* Configure the server and the mailsettings as you wish:

  ```
  $ cp course/settings.py.example course/settings.py
  $ cp user/mailsettings.py.example user/mailsettings.py
  $ make migrate
  ```

* Launch the program with

  ```
  $ env/bin/python manage.py runserver
  ```

* You now can login with the super user **foo** and password **bar**

## License

This software is licensed with the BSD3 license.
