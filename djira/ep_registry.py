# -*- coding: utf-8 -*-

# $Id:$

"""Endpoint registry.

This module provides interaction with the endpoints registry:

- initialization: calls ``get_endpoints`` on each registered plugin
  and populates the registry. It takes care of handling name
  collisions.

- querying: allows to check the registered endpoints.

"""

from __future__ import print_function
from __future__ import unicode_literals

import itertools

from .common import EndPoint
from .common import get_plugin_manager
from .schema import get_schema_spec


# endpoints registry
_endpoints = None


def get_endpoint_by_name(name):
    """Returns an endpoint given a name.

    If theres no endpoint named ``name`` returns ``None``.

    """
    global _endpoints

    if _endpoints is None:
        pm = get_plugin_manager()
        _endpoints = {i.name: i for i in _DEFAULT_ENDPOINTS}
        _update_endpoints(_endpoints, pm.hook.get_endpoints())

    return _endpoints.get(name, None)

#             _            _
#  _ __  _ __(_)_   ____ _| |_ ___
# | '_ \| '__| \ \ / / _` | __/ _ \
# | |_) | |  | |\ V / (_| | ||  __/
# | .__/|_|  |_| \_/ \__,_|\__\___|
# |_|

# builtin endpoints


def ep_list():
    """List available endpoints.

    """

    res = []
    for ep in sorted(_endpoints.values(), key=lambda x: x.name):
        if ep.request_schema:
            args_doc = get_schema_spec(ep.request_schema)
        else:
            args_doc = {}
        if ep.response_schema:
            response_doc = get_schema_spec(ep.response_schema)
        else:
            response_doc = {}
        res.append({
            "name": ep.name,
            "description": ep.doc,
            "parameters": args_doc,
            "response": response_doc,
        })
    return res


def ep_ping():
    """Check service availability.

    """
    return "pong"


_DEFAULT_ENDPOINTS = [
    EndPoint(ep_list, name="__list__", doc="List available endpoints."),
    EndPoint(ep_ping, name="__ping__", doc="Test service availability."),
]


# helper functions

def _update_endpoints(res, l):
    for ep in itertools.chain(*l):
        if not isinstance(ep, EndPoint):
            raise ValueError("not an endpoint {!r}".format(ep))
        if ep.name in res:
            raise ValueError("endpoint already exists: {}".format(ep.name))
        res[ep.name] = ep
