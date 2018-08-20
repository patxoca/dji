# -*- coding: utf-8 -*-

# $Id: __init__.py 1251 2016-03-25 14:10:28Z alex $

import itertools

from django.conf import settings
from django.http.response import HttpResponseForbidden
from django.http.response import HttpResponseNotFound
from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods

from .common import EndPoint
from .common import get_plugin_manager


@require_http_methods(["GET", "HEAD"])
def dispatcher(request, name):
    """Dispatches the call to the endpoint.

    """
    global _endpoints

    if not settings.DEBUG:
        return HttpResponseForbidden()

    if _endpoints is None:
        pm = get_plugin_manager()
        _endpoints = {i.name: i for i in _DEFAULT_ENDPOINTS}
        _update_endpoints(_endpoints, pm.hook.get_endpoints())

    ep = _endpoints.get(name, None)
    if ep is None:
        return HttpResponseNotFound(name)

    # params = ep.request_schema.validate(request.GET)
    params = request.GET
    res = ep.function(**params)
    return JsonResponse(res, encoder=ep.encoder, safe=False)


#             _            _
#  _ __  _ __(_)_   ____ _| |_ ___
# | '_ \| '__| \ \ / / _` | __/ _ \
# | |_) | |  | |\ V / (_| | ||  __/
# | .__/|_|  |_| \_/ \__,_|\__\___|
# |_|

_endpoints = None


def _ep_list():
    "List available endpoints."
    res = []
    for ep in sorted(_endpoints.values(), key=lambda x: x.name):
        res.append({"name": ep.name, "doc": ep.doc, "args": "TODO"})
    return res


def _ep_ping():
    return "pong"


_DEFAULT_ENDPOINTS = [
    EndPoint(_ep_list, name="__list__", doc="List available endpoints."),
    EndPoint(_ep_ping, name="__ping__", doc="Test service availability."),
]


def _update_endpoints(res, l):
    for ep in itertools.chain(*l):
        if not isinstance(ep, EndPoint):
            raise ValueError("not an endpoint {!r}".format(ep))
        if ep.name in res:
            raise ValueError("endpoint already exists: {}".format(ep.name))
        res[ep.name] = ep
