# -*- coding: utf-8 -*-

# $Id:$

from __future__ import print_function
from __future__ import unicode_literals

import functools
import inspect

# FIXME: en django 2.x s'ha refactoritzat tot el tema de les URLs i
# aquests imports fallen
from django.urls.resolvers import RegexURLPattern
from django.urls.resolvers import RegexURLResolver
from django.urls import get_resolver
from django.urls import get_urlconf

from ..common import EndPoint
from ..common import hookimpl


@hookimpl
def get_endpoints():
    return (
        EndPoint(get_urls_details),
    )


def get_urls_details():
    """Return a list with the models names."""
    patterns = []
    _get_url_patterns(get_resolver(get_urlconf()), patterns, "")
    res = {}
    for i in patterns:
        info = {
            "url_name": i["pattern"].name,
            "pattern": i["url"],
        }
        info.update(_get_callback_info(i["pattern"].callback))
        res[i["pattern"].name] = info
    return res


def _get_url_patterns(resolver, result, prefix):
    for i in resolver.url_patterns:
        if isinstance(i, RegexURLPattern):
            result.append({
                "url": _cleanup_pattern(prefix + i.regex.pattern),
                "pattern": i,
            })
        elif isinstance(i, RegexURLResolver):
            _get_url_patterns(i, result, _cleanup_pattern(prefix + i.regex.pattern))
        else:
            raise TypeError(type(i))


def _get_callback_info(cb):
    cb_name = None
    cb_path = None
    cb_lineno = None
    if hasattr(cb, "__name__"):
        cb_name = cb.__name__
    while True:
        if hasattr(cb, "__wrapped__"):
            cb = cb.__wrapped__
        elif hasattr(cb, "view_class"):
            cb = cb.view_class
        elif isinstance(cb, functools.partial):
            cb = cb.func
        else:
            break
    try:
        cb_path = inspect.getsourcefile(cb)
        cb_lineno = inspect.getsourcelines(cb)[1]
    except TypeError:
        pass
    return {
        "callback_name": cb_name,
        "callback_path": cb_path,
        "callback_lineno": cb_lineno,
    }


def _cleanup_pattern(pattern):
    return pattern.replace("^", "").replace("$", "")
