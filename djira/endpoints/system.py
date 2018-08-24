# -*- coding: utf-8 -*-

# $Id:$

from __future__ import print_function
from __future__ import unicode_literals

import json
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
    return {
        "django": django.__path__[0],
        "django_settings": _get_settings(),
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
