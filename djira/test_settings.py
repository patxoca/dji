# -*- coding: utf-8 -*-

# $Id: $

# Settings to be used when running unit tests
# python manage.py test --settings=djira.test_settings djira

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    }
}

SECRET_KEY = "Tests don't require a really s3cr3t k3y ;)"

INSTALLED_APPS = (
    # Put any other apps that your app depends on here

    #BEGIN:installed_apps
    # "django.contrib.auth",
    # "django.contrib.contenttypes",
    # "django.contrib.sessions",
    # "django.contrib.messages",
    # "hera_django",
    # "hera_formsng",
    # "hera_skin",
    # "hera_utils",
    #END:installed_apps

    "djira",
    "djira.tests",
)

SITE_ID = 1

MIDDLEWARE_CLASSES = (
    # "django.contrib.sessions.middleware.SessionMiddleware",
    # "django.contrib.auth.middleware.AuthenticationMiddleware",
    # "django.contrib.messages.middleware.MessageMiddleware",
)

ROOT_URLCONF = "djira.test_urls"

TEMPLATES = ({
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "APP_DIRS": True,
    "OPTIONS": {
        "context_processors": (
            'django.contrib.messages.context_processors.messages',
        ),
    },
}, )
