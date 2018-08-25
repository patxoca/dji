# -*- coding: utf-8 -*-

# $Id:$

from __future__ import print_function
from __future__ import unicode_literals

from django.apps import apps

from ..common import EndPoint
from ..common import hookimpl
from .. import schema as S


@hookimpl
def get_endpoints():
    return (
        EndPoint(get_apps_list),
        EndPoint(get_apps_details, request_schema=get_apps_details_schema),
    )


def get_apps_list():
    """Returns a list with the labels of the installed apps.

    """
    return sorted(apps.app_configs.keys())


get_apps_details_schema = S.Schema(
    schema=dict(
        labels=S.List(S.String(doc="app label"))
    )
)


def get_apps_details(labels):
    """Returns details about the given apps.

    """
    res = {}
    for app_label in labels:
        try:
            app = apps.get_app_config(app_label)
        except LookupError:
            details = None
        else:
            details = _get_app_detail(app)
        res[app_label] = details
    return res


def _get_app_detail(app):
    return {
        "label": app.label,
        "models": _get_models(app),
        "name": app.name,
        "path": app.path,
        "verbose_name": app.verbose_name,
    }


def _get_models(app):
    return sorted([
        class_._meta.object_name
        for class_ in app.models.values()
    ])
