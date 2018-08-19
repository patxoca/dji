# -*- coding: utf-8 -*-

# $Id:$

#BEGIN:import
from django.apps import AppConfig

#END:import


class MyAppConfig(AppConfig):
    name = "djira"
    verbose_name = u"djira"
    def ready(self):
        #MARKER:ready_import
        #MARKER:ready
        pass
