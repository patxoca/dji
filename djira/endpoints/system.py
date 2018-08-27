# -*- coding: utf-8 -*-

# $Id:$

from __future__ import print_function
from __future__ import unicode_literals

import importlib
import json
import os
import sys

import django
from django.conf import settings

from ..common import EndPoint
from ..common import hookimpl


_cached_settings = None


@hookimpl
def get_endpoints():
    return (
        EndPoint(get_system_info),
    )


def get_system_info():
    """Return a dictionary with assorted system information.

    """
    settings_module_name = os.environ.get("DJANGO_SETTINGS_MODULE", None)
    if settings_module_name:
        try:
            settings_module = importlib.import_module(settings_module_name)
        except ModuleNotFoundError:
            project_root = None
        else:
            settings_module_path = settings_module.__file__
            if settings_module_path.endswith(".pyc"):
                settings_module_path = settings_module_path[:-1]
            project_root = os.path.dirname(os.path.dirname(settings_module.__file__))
    else:
        project_root = None

    return {
        "django": django.__path__[0],
        "django_project_root": project_root,
        "django_settings": _get_settings(),
        "django_settings_module": settings_module_name,
        "django_settings_path": settings_module_path,
        "django_version": django.VERSION,
        "python": sys.executable,
        "python_version": list(sys.version_info),
    }


def _get_settings():
    """Returns a dictionary with the settings.

    The returned dictionary i guaranteed to be json serializable, the
    values that aren't are converted to string with ``repr``.

    The dictionary is initialized in the first call and reused in
    subsequent calls.

    """
    global _cached_settings

    if _cached_settings is None:
        res = {}
        for i in dir(settings):
            if i.startswith("_"):
                continue
            v = getattr(settings, i)
            try:
                json.dumps(v)
            except TypeError:
                v = repr(v)
            res[i] = v
        _cached_settings = res
    return _cached_settings
