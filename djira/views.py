# -*- coding: utf-8 -*-

# $Id: __init__.py 1251 2016-03-25 14:10:28Z alex $

import itertools
import traceback

from django.conf import settings
from django.http.response import HttpResponseForbidden
from django.http.response import HttpResponseNotFound
from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods

from .common import EndPoint
from .common import get_plugin_manager
from .common import logger
from .validators import SchemaError


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

    # get endpoint
    ep = _endpoints.get(name, None)
    if ep is None:
        return HttpResponseNotFound(name)

    # validate arguments
    if ep.request_schema:
        try:
            params = ep.request_schema.to_python(request.GET)
        except SchemaError as e:
            logger.info("Error in arguments: %s", e.args[0])
            return _error_response(400, e.args[0])
        except Exception as e:
            logger.error(
                "Unexpected error validating arguments: endpoint='%s', GET=%r",
                name, request.GET,
                exc_info=True
            )
            return _error_response(500, e.args[0], details=e)
    else:
        params = {}

    # run endpoint
    try:
        res = ep.function(**params)
    except Exception as e:
        logger.error(
            "Unexpected error running endpoint: endpoint='%s', kwargs=%r",
            name, params,
            exc_info=True
        )
        return _error_response(500, e.args[0], details=e)

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


def _error_response(http_status, description, error_code=None, details=None):
    if isinstance(details, Exception):
        details = traceback.format_exc()
    response = {
        "message": description,
        "code": error_code,
        "details": details,
    }
    return JsonResponse(response, status=http_status)
