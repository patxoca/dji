# -*- coding: utf-8 -*-

# $Id:$

#BEGIN:import
from django.apps import AppConfig
import pluggy

from . import hookspec
from .common import PROJECT_NAME

from . import demo
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
        pm.load_setuptools_entrypoints(PROJECT_NAME)
        pm.register(demo)

        pm.hook.initialize()
