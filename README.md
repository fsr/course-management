# A homegrown course management system

This repository houses the source code that runs the [course management system](https://kurse.ifsr.de) operated by the [student representatives](https://www.ifsr.de) of the computer science department. It can be used to manage programming courses or pretty much every other event that has a limited number of attendees and should therefore offer a registration.

## Technical tidbits

The course system is written in [Django](https://djangoproject.com/) and uses the [Litera](https://bootswatch.com/litera/) Bootstrap theme.

## Setting up a development environment

1. In order to use this project, you need `python3` and on your system. Install them via your distributions' package manager. If you want, you can use `virtualenv` to not pollute your working environment too much.
2. Copy the example configuration and mail settings and customize them as you see fit:
```
cp course/settings.py.example course/settings.py
cp user/mailsettings.py.example user/mailsettings.py
```
3. Install any Python dependencies via `pip3 install -r requirements.txt`.
3. Run `python3 manage.py migrate` to apply the database migrations and `python3 manage.py loaddata courses` to load a sample data set.
4. Fire up the development server with `python3 manage.py runserver`.
5. You now can login with the super user **foo** and password **bar**

Another test user is available by logging in as `test: test`.

## Changing the database model

When changing the database model make sure that the fixture located in `course/fixtures/courses.yaml` still works.
If not, export a new version of the fixture using the command
```
python manage.py dumpdata --format yaml --exclude contenttypes --output course/fixtures/courses.yaml
```
It should always include the two aforementioned test users and a set of example courses.

## License

This software is licensed with the BSD3 license. See the `LICENSE` file for more information.
