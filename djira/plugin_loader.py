# -*- coding: utf-8 -*-

# $Id:$

"""Plugin loaders.

A plugin loader implements the policy used to discover and load
plugins.

A loader it's just a callable that receives a ``plugin_manager`` as
argument and populates it with plugins.

"""

from __future__ import print_function
from __future__ import unicode_literals

from importlib import import_module

from .common import get_config_value
from .common import PROJECT_NAME


def entry_points(plugin_manager):
    """Load plugins from setuptools' entry points.

    Loads the plugins registered as ``djira`` entry points.

    """
    plugin_manager.load_setuptools_entrypoints(PROJECT_NAME)


def django_config(plugin_manager):
    """Load plugins listed in the configuration.

    Loads the plugins listed in the djira's configuration
    ``enabled_plugins``. Each entry in the list is the name (an
    string) of a module.

    """
    for module_name in get_config_value("enabled_plugins", []):
        module = import_module(module_name)
        plugin_manager.register(module)
