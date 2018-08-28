.. -*- mode: rst; ispell-local-dictionary: "en" -*-

.. $Id:$


Introduction
============

Django app that exposes some internals through a REST API. Intended
for development tools comsumption.

The first objective is writing an emacs plugin that helps developing
django apps.


Installation
============

To install from *pypi* just run ``pip install djira``.

To install de development version clone the git repo:

.. code-block:: bash

   git clone https://github.com/patxoca/djira.git


From a virtualenv (recommended), install the package in development
mode:

.. code-block:: bash

   cd djira
   python setup.py develop


Configuration
=============

Add ``djira`` to ``INSTALLED_APPS`` in your project's config and
include djira URLs in your root url definition:

.. code-block:: python

   urlpatterns = [
       ...
       url(r"^__djira__/", include("djira.urls")),
       ...
   ]


In order to test the installation start the development server and
point a browser to ``http://localhost:8000/__djira__/__ping__/``, this
should display a ``pong`` response.


Calling an endpoint
===================

As seen in the previous section, calling an endpoint is just a matter
of executing a ``GET`` request on some URL.

**Warning**: ``djira`` provides a read-only API so it only accepts
``GET`` and ``HEAD`` requests.

In order to improve readability the output from the following examples
has been *prettyfied*. Depending on the plugins you have enabled the
output may be different.

.. code-block:: bash

   $ curl http://localhost:8000/__djira__/__ping__/
   "pong"


If you get no output make sure you have included the trailing slash in
the URL.

The API can be queried to get details about the endpoints. The
``__list__`` endpoint returns info about the registered endpoints:

.. code-block:: bash

   $ curl http://localhost:8000/__djira__/__list__/
   [
     {
       "name": "__list__",
       "description": "List available endpoints.",
       "parameters": {}
     },
     {
       "name": "__ping__",
       "description": "Test service availability.",
       "parameters": {}
     },
     {
       "name": "__version__",
       "description": "Get djira API version.",
       "parameters": {}
     },
     {
       "name": "get_model_info",
       "description": "Return a dict with info about the given model.",
       "parameters": {
         "description": "",
         "type": "schema",
         "extra": {
           "model_id": {
             "description": "Model name.",
             "type": "string",
             "required": true
           }
         }
       }
     },
     {
       "name": "get_models_names",
       "description": "Return a list with the models names.",
       "parameters": {}
     }
   ]


If the endpoint is omitted it is assumed to be ``__list__``.

Arguments are passed in the query string:

.. code-block:: bash

   $ curl http://localhost:8000/__djira__/get_model_info/?model_id=FooBarModel
   {
     "name": [
       "FooBarModel"
     ],
     "verbose_name": "Some descriptive text",
     "fields": [
       {
         "name": "my_field",
         "type": "int"
       }
     ]
   }


Available endpoints
===================

Only the ``__list__``, ``__ping__`` and ``__version__`` endpoints are
guaranteed to be available, the remaining endpoints (including those
provided by ``djira`` itself) are implemented as plugins and can be
replaced or removed on a per project basis.


Plugins
=======

I want ``djira`` to be easily extensible so you can add your own
endpoints to the API without getting a headache.

``djira`` uses ``pluggy`` in order to manage the plugins.


Writing plugins
---------------

Take a look at the ``hookspec.py`` module to see what the current
specification of the plugin API is.

Take a look at the ``demo.py`` module for an example.

Take a look at the `pluggy docs <https://pluggy.readthedocs.io/en/latest/>`_
for extra details.

**Warning**: endpoints with *dunder* names are reserved for internal
usage.


Loading plugins
---------------

In order to discover and load plugins ``djira`` implements two plugin
loaders:

- ``entry_points``: loads **all** plugins declared in a ``djira`` `entry
  point <https://setuptools.readthedocs.io/en/latest/setuptools.html#dynamic-discovery-of-services-and-plugins>`_.
  Load order is undefined. This is the default loader.

- ``django_config``: loads all plugins listed in the
  ``enabled_plugins`` configuracion option. This loader gives finer
  control on what plugins are loaded on what order at the expense
  of increased verbosity.

The plugin loader is configured in ``settings.py``:

.. code-block:: python

   DJIRA = {
       "plugin_loader": "djira.plugin_loader.django_config",
       "enabled_plugins": ["djira.demo"],
   }

This example enables the ``djira.demo`` plugin.
