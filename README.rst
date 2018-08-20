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

Clone the git repo:

.. code-block:: bash

   git clone https://github.com/patxoca/djira.git


From a virtualenv (recommended), install the package in development
mode:

.. code-block:: bash

   cd djira
   python setup.py develop


Add the ``djira`` to ``INSTALLED_APPS`` in your project's config and
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

Take a look at the `djira docs <https://pluggy.readthedocs.io/en/latest/>`_
for extra details.

.. warning:: endpoints with *dunder* names are reserved for internal
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
  control on what plugins are loaded and on the order at the expense
  of some verbosity.

The plugin loader is configured in ``settings.py``:

.. code-block:: python

   DJIRA = {
       "plugin_loader": "djira.plugin_loader.django_config",
       "enabled_plugins": ["djira.demo"],
   }

This example enables the ``djira.demo`` plugin.
