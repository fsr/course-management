# The real course-management

## Gettin' started

 * install requirements

```bash
./install.sh
```

 * go to folder *src*
 * Initialize the database
```bash
 python3 manage.py migrate
```

 * Add some fixtures
```bash
 python3 manage.py loaddata course_management/fixtures/courses.yaml
```

 * Start the server
```bash
 python3 manage.py runserver
```

* You now can login with the super user **foo** pass: *bar*
