# A homegrown course management system

This repository houses the source code that runs the [course management system](https://kurse.ifsr.de) operated by the [student representatives](https://www.ifsr.de) of the computer science department at [TU Dresden](https://tu-dresden.de). It can be used to manage programming courses or pretty much every other event that has a limited number of attendees and should therefore offer a registration.

## Technical tidbits

The course system is written in [Django](https://djangoproject.com/) and uses the [Litera](https://bootswatch.com/litera/) Bootstrap theme.

For more details on the design decisions taken and the general structure of the application, please refer to the [**design overview**](./OVERVIEW.md).

## Setting up a development environment

1. In order to use this project, you need `python3` and on your system. Install them via your distributions' package manager. If you want, you can use `virtualenv` to not pollute your working environment too much.
2. Copy the example configuration and mail settings and customize them as you see fit:
```
cp course/settings.py.example course/settings.py
cp user/mailsettings.py.example user/mailsettings.py
```
3. Install any Python dependencies via `pip3 install -r requirements.txt`.
4. Run `python3 manage.py migrate` to apply the database migrations.
5. Run `python3 manage.py loaddata courses` to load a sample data set.
6. Fire up the development server with `python3 manage.py runserver`.
7. You now can login with the super user **foo** and password **bar**

Another test user is available by logging in as `test: test`.

Opening `http://[project url]/admin` in your browser gives you access to the standard admin interface of Django which you can use to make manual changes to the database.

## Changing the database model

When changing the database model make sure that the fixture located in `course/fixtures/courses.yaml` still works.
If not, export a new version of the fixture using the command
```
python manage.py dumpdata --format yaml --exclude contenttypes --output course/fixtures/courses.yaml
```
It should always include the two aforementioned test users and a set of example courses.

## Deployment

To deploy the application in an productive environment, using a SQLite database is discouraged.
The amount of concurrent users during registration frequently overwhelms the simplistic architecture and therefore, a MySQL/Postgres database should be preferred.
Be sure to change the `settings.py` configuration accordingly.

Otherwise, just follow steps 1-4 from the checklist above, then follow the standard [instructions for deploying a Django application](https://docs.djangoproject.com/en/3.2/howto/deployment/) and check the [deployment checklist](https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/).

Run the `python3 manage.py createsuperuser` command to create a root user for the application to be able to assign administrative privileges to new users.
Admin rights may in general only be granted from the `http://[site url]/admin` page by selecting the appropriate user there and giving them staff/superuser rights.

## License

This software is licensed with the BSD3 license. See the `LICENSE` file for more information.

