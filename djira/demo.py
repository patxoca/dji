# -*- coding: utf-8 -*-

# $Id:$

# sample plugin for testing/demonstration purpose

from __future__ import print_function
from __future__ import unicode_literals

from .common import EndPoint
from .common import hookimpl
from . import schema as S


@hookimpl
def initialize():
    print("demo: initialize")


@hookimpl
def get_endpoints():
    return (
        EndPoint(get_models_names, response_schema=get_models_names_response_schema),
        EndPoint(get_model_info, request_schema=get_model_info_schema),
    )


get_models_names_response_schema = S.List(S.String(), doc="list of model names")


def get_models_names():
    """Return a list with the models names."""
    return ["foo", "bar", "baz"]


get_model_info_schema = S.Schema(
    schema=dict(
        model_id=S.String(doc="Model name."),
    ),
)


def get_model_info(model_id):
    """Return a dict with info about the given model."""
    return {
        "name": model_id,
        "verbose_name": "Some descriptive text",
        "fields": [
            {"name": "my_field", "type": "int"},
        ]
    }
