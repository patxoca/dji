# -*- coding: utf-8 -*-

# $Id:$

#BEGIN:import
from importlib import import_module

from django.apps import AppConfig
from django.core.exceptions import ImproperlyConfigured
import pluggy

from . import hookspec
from .common import get_config_value
from .common import PROJECT_NAME
#END:import


class DjiraAppConfig(AppConfig):
    name = PROJECT_NAME
    verbose_name = PROJECT_NAME

    def ready(self):
        #MARKER:ready_import
        #MARKER:ready
        pm = pluggy.PluginManager(PROJECT_NAME)
        self.plugin_manager = pm
        pm.add_hookspecs(hookspec)
        loader = self._get_plugin_loader()
        loader(pm)

        pm.hook.initialize()

    def _get_plugin_loader(self):
        loader_fqn = get_config_value("plugin_loader", "djira.plugin_loader.entry_points")
        module_name, loader_name = loader_fqn.rsplit(".", 1)
        module = import_module(module_name)
        if not hasattr(module, loader_name):
            raise ImproperlyConfigured(
                "DJIRA.plugin_loader: loader not found '{}'".format(loader_name)
            )
        return getattr(module, loader_name)
