# A homegrown course management system

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

## License

This software is licensed with the BSD3 license. See the `LICENSE` file for more information.
