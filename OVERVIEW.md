# Design Overview

This document tries to detail some of the design decisions taken during the development and give people an overview over the code base in general.

Bear in mind that the project has accumulated quite some history by now.
It originally was created by some students as part of an official course at TUD. Let's call it version _0.1_.
Unfortunately, the result was borderline unusable, even after numerous hasty hotfixes applied.
Thus, some time later, the system was rewritten from scratch using Django over a weekend-long Hackathon.
The resulting system (version _1.0_) was a little rough around the edges and had problems of its own, but it at least worked semi-reliably (aside from some logic errors in the database that went unnoticed.
However, the UI design was terrible and some problems in the backend required an extensive rework of some functionality.
After the final [massive PR](https://github.com/fsr/course-management/pull/97), version 2.0, the current iteration was born.

## Project Structure

The project consists of two different Django applications, one for user management and one for managing courses.
This is for legacy reasons, it was originally planned to have a "polls" application as well and thus user management was factored out of the course management part.

Each application follows the standard Django project structure, as shown on the example of the `course` application:

```text
course/
├── __init__.py
├── admin.py                :: setup of the admin page found on /admin
├── fixtures                :: test data for use in development
├── forms.py                :: defines all forms used in the application (e.g. course creation, ...)
├── migrations              :: contains (mostly automatically generated) database migrations that
│                              create the database according to the model
├── models                  :: defines the data structures used in the applications that should be
│                              represented as persistent data in the database
├── settings.py.example     :: application settings
├── templates               :: templates filled by Django to deliver a page
├── tests                   :: lol
├── translation.py          :: registers translators
├── urls.py                 :: defines which URL route is mapped to which function
├── util                    :: helper functions for use throughout the code
└── views                   :: functions that render the pages sent back to the user
```

For details about the project structure or specific topics, I can recommend looking through the Django documentation.
It's an incredibly good source for information, e.g. on [Models](https://docs.djangoproject.com/en/3.2/topics/db/models/).
The [landing page](https://docs.djangoproject.com/en/3.2/) also details how the different layers (template, view and model layer) are supposed to work.
The whole project has been designed following the tutorials there, so hopefully understanding the code can be achieved by understanding the docs.

The templates in the project use the built-in Django template engine, which is relatively similar to the Jinja templating engine.
Please see the [template documentation](https://docs.djangoproject.com/en/3.2/topics/templates/) for more information.

The site uses the [built-in admin site](https://docs.djangoproject.com/en/3.2/ref/contrib/admin/) to provide easy access to the database layer and allow for manual changes (i.e., password resets) without too much of a hassle.

### Changing a specific functionality

To change the specific behavior for a certain view, it's usually good to look up which function handles the URL you want to change.
Then look up the function in the `views` module and see what functions may be used in generating the view.
From there, you'll see the templates used to generate the site and the models used to represent the data.

Bear in mind that changes to the model are very invasive as they require a change to the underlying database.


## Design Decisions 

_a.k.a. Why is everything different from what I expected?_

### Why does xy not conform to established UI design principles?

Because I (@feliix42) did the latest UI revamp and I'm a backend person.
I tried getting someone experienced (or at least knowledgable) to do the design but couldn't find anyone in 2 years of searching.
Hence, I picked a CSS template I liked and got to work.

If you think something should look/work differently, _please_ feel free to change it! It's much appreciated! :)

### Why is this project using its own user management?

During development of the course system there were three main options for handling user management:

1. Re-use the FSR-internal user management (LDAP).
2. Use the TUD-provided Shibboleth authentication.
3. Use Github (or other `$network`) authentication.
4. Have our own user management specific for this project.

**Option 1** was never really feasible, because our internal user management at the time was not designed to take in hundreds or thousands of new users not connected to the iFSR.
Our LDAP was never designed to handle users that are in no way associated to the iFSR and would thus have to be completely revamped.
Also, this separation of concerns makes the project potentially re-usable for others and minimizes the effect of a potential security breach in one system to keep core FSR systems operational.

**Option 2** sounds like a good idea at first (we don't have to store any credentials etc), but comes with (painful) problems of its own:
- We would probably have to undergo extensive buercratic processes to get the Shibboleth authentication authorized and working.
- External people would find themselves unable to create and account or use the system, which was a use case multiple times in the past.
Additionally, nobody really wanted to put up with this process during development, as Django brings its own, easy-to-use user management and this was a Hackathon & Hobby project after all.

**Option 3** contradicts everything we wanted to offer the users: A privacy-friendly open system for course registration.

Thus, **Option 4** was chosen.

### Why do you host everything yourself?

Privacy has always been a major concern for us, and therefore serving scripts/style sheets from external sources is a no-go for us.
