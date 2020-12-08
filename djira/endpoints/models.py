# -*- coding: utf-8 -*-

# $Id:$

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from django.db.models import NOT_PROVIDED

from ..common import EndPoint
from ..common import hookimpl
from .. import schema as S


@hookimpl
def get_endpoints():
    return (
        EndPoint(get_model_details, request_schema=get_model_details_schema),
    )


get_model_details_schema = S.Schema(
    schema=dict(
        model=S.DottedModelName(doc="model name"),
    )
)


def get_model_details(model):
    """Returns an object with details about a model.

    """
    meta = model._meta
    return {
        "abstract": meta.abstract,
        "app_label": meta.app_label,
        "auto_created": meta.auto_created,
        "auto_field": meta.auto_field.name if meta.auto_field else None,
        "concrete_fields": [i.name for i in meta.concrete_fields],
        "db_table": meta.db_table,
        "db_tablespace": meta.db_tablespace,
        "default_permissions": meta.default_permissions,
        "default_related_name": meta.default_related_name,
        "fields": {i.name: _serialize_field(i) for i in meta.fields},
        "has_auto_field": meta.has_auto_field,
        "index_together": meta.index_together,
        "installed": meta.installed,
        "label": meta.label,
        "label_lower": meta.label_lower,
        "managed": meta.managed,
        "manager_inheritance_from_future": meta.manager_inheritance_from_future,
        "model_name": meta.model_name,
        "object_name": meta.object_name,
        "ordering": meta.ordering,
        "permissions": meta.permissions,
        "pk": meta.pk.name,
        "unique_together": meta.unique_together,
        "verbose_name": meta.verbose_name,
        "verbose_name_plural": meta.verbose_name_plural,
        "verbose_name_raw": meta.verbose_name_raw,
        "virtual_fields": meta.virtual_fields,
    }


FIELD_ATTRS = (
    "attname", "auto_now", "auto_now_add", "blank", "choices",
    "column", "description", "editable", "empty_strings_allowed",
    "encoding", "help_text", "hidden", "max_length", "name", "null",
    "primary_key", "unique", "unique_for_date", "unique_for_month",
    "unique_for_year", "verbose_name",
)


def _serialize_field(model):
    res = {}
    for i in FIELD_ATTRS:
        if hasattr(model, i):
            res[i] = getattr(model, i)

    if model.default is NOT_PROVIDED:
        default = None
    else:
        default = model.default
    res["default"] = default

    return res
