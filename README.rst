django-db-sanitizer - Anonymizes sensitive database data for Django projects
============================================================================

:Authors:
  Resulto Developpement Web Inc.
:Version: 0.1.0

This project's main goal is to provide a way to anonymize the data of
specific database fields by explicitly configuring said fields with specific
anonymization strategies.

The anonymization process provides a "Production-like" copy of your database
without sensitive information which can then be used in a development
environment.


Requirements
------------

django-db-sanitizer works and has been tested with Python 2.7 and 3.5.
It requires Django 1.8+ and fake-factory 0.5.7+.

Installation
------------

Install the library
~~~~~~~~~~~~~~~~~~~

::

    pip install django-db-sanitizer


Add the library to your INSTALLED_APPS in your Django Settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django_db_sanitizer',
    )


Important Notes
---------------

**DO NOT RUN IN YOUR PRODUCTION ENVIRONMENT!**

In its current state, django-db-sanitizer will run its sanitizing command and
operations on your default database.

While there are plans to investigate the possibility of allowing the sanitizing
process to run on alternate databases, this is not yet implemented.

It is recommended to run django-db-sanitizer on a copy of your application and
database running on your local machine.

Please read the **Usage** section below for more information.

Usage
-----

Creating db_sanitizer.py
~~~~~~~~~~~~~~~~~~~~~~~~

Configuration of django-db-sanitizer works similarly to the configuration of
the Django admin site.

To use django-db-sanitizer for one of your Django apps, create a
``db_sanitizer.py`` file into said Django app just as you would create an
``admin.py`` file for the Django admin site.

Model and field declarations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Inside the ``db_sanitizer.py`` file of your app, you must explicitly register
which fields of which models will be sanitized using an explicitly declared
Sanitizer class.

In the following example, the ``notes`` text field of the ``Profile`` class
will be sanitized using the ``LoremIpsumSanitizer`` sanitizing strategy,
filling the contents of the field with *Lorem Ipsum* text.

::

    from django_db_sanitizer import sanitizer_registry, LoremIpsumSanitizer

    from my_app.models import Profile

    sanitizer_registry.register(Profile, ["notes"], LoremIpsumSanitizer)

Customizing the sanitizing process
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

django-db-sanitizer is meant to be easy to extend. It is easily possible to
override or extend classes from django-db-sanitizer to:

- Filter querysets on which the sanitizing process is applied
- Modify existing Sanitizer classes to alter their behavior
- Add your own new Sanitizer classes
- Add your own Updater classes to control how values are saved to the database
- And more...

Please refer to the ``test_app`` in django-db-sanitizer's ``test_project``
within the repository for a number of examples on how to achieve this.

Running the sanitizing process
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Currently, the only way to run the sanitizing process is to use the included
Django command, like so:

::

    python manage.py sanitize_my_database

This command does not use or require any arguments for the time being.

Please note that the sanitizing process is irreversible. It is recommended to
run django-db-sanitizer on a copy of your application and database running on
your local machine.

License
-------

This software is licensed under the `New BSD License`. See the `LICENSE` file
in the repository for the full license text.
