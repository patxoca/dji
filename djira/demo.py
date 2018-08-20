# -*- coding: utf-8 -*-

# $Id:$

# sample plugin for testing/demonstration purpose

from __future__ import print_function
from __future__ import unicode_literals

from .common import EndPoint
from .common import hookimpl


@hookimpl
def initialize():
    print("demo: initialize")


@hookimpl
def get_endpoints():
    return (
        EndPoint(get_models_names),
        EndPoint(get_model_info, request_schema="TODO"),
    )


def get_models_names():
    """Return a list with the models names."""
    return ["foo", "bar", "baz"]


def get_model_info(model_id):
    """Return a dict with info about the given model."""
    return {
        "name": model_id,
        "verbose_name": "Some descriptive text",
        "fields": [
            {"name": "my_field", "type": "int"},
        ]
    }
