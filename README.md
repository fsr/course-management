# A homegrown course management system

**The project is currently undergoing a major overhaul which is mainly UI-focussed but touches almost every aspect of the core code in some way. You can find the current progress [here](https://www.notion.so/feliix42/Course-Manager-Overhaul-d0e2446ad6504b28bb734eab74900263).**

This repository is the home of the [course management system](https://www.ifsr.de/kurse) source code, used by us to manage programming courses we provide to the students of our faculty.

## Setting up a development environment

1. In order to use this project, you need `python3` and [`sassc`](https://github.com/sass/sassc) on your system. Install them via your distributions' package manager.
2. Copy the example configuration and mail settings and customize them as you see fit:
```
cp course/settings.py.example course/settings.py
cp user/mailsettings.py.example user/mailsettings.py
```
3. Compile the sass files and install any Python dependencies via `make`.
3. Run `make migrate` to apply the database migrations and load a sample data set.
4. Launch the program with `env/bin/python manage.py runserver`.
5. You now can login with the super user **foo** and password **bar**

Another test user is available by logging in as `test: test`.

## Changing the database model

When chaning the database model make sure that the fixture located in `course/fixtures/courses.yaml` still works.
If not, export a new version of the fixture using the command
```
python manage.py dumpdata --format yaml --exclude contenttypes --output course/fixtures/courses.yaml
```
It should always include the two aforementioned test users and a set of example courses.

## License

This software is licensed with the BSD3 license. See the `LICENSE` file for more information.
