# -*- coding: utf-8 -*-

# $Id:$

"""The schema allows to specify formally the call interface for an
endpoint.

Example/Motivation: TODO

How missing/undefined values work: TODO


"""

from __future__ import print_function
from __future__ import unicode_literals

import functools

from django.utils.datastructures import MultiValueDict

from . import validators as V

# marker for missing values
_UNDEFINED = object()


def handle_undefined_value(f):
    @functools.wraps(f)
    def decorator(self, value):
        if value is _UNDEFINED:
            if self.default is _UNDEFINED:
                raise V.SchemaError("missing required value")
            else:
                # NOTE: just to be safe, assume that the default value
                # may contain errors
                value = self.default

        return f(self, value)
    return decorator


class _Type(object):
    """Base class for schema types.

    """

    type_name = None
    python_type = None

    def __init__(self, default=_UNDEFINED, doc="", validators=()):
        self.default = default
        self.doc = doc
        self._validators = list(validators)  # make a copy

    @handle_undefined_value
    def to_python(self, value):
        """Converts a value from the request to a python type.

        """
        try:
            value = self.python_type(value)
        except (ValueError, TypeError) as e:
            raise V.SchemaError(*e.args)

        return self._apply_validators(value)

    def _apply_validators(self, value):
        for validator in self._validators:
            value = validator(value)
        return value


class Int(_Type):
    type_name = "int"
    python_type = int


class Float(_Type):
    type_name = "float"
    python_type = float


class String(_Type):
    type_name = "string"
    python_type = str


class List(_Type):
    type_name = "list"
    python_type = list

    def __init__(self, item_type, *args, **kwargs):
        super(List, self).__init__(*args, **kwargs)
        self._item_type = item_type

    @handle_undefined_value
    def to_python(self, value):
        to_python = self._item_type.to_python
        res = [to_python(i) for i in value]
        return self._apply_validators(res)


class Schema(_Type):
    type_name = "schema"
    python_type = dict

    def __init__(self, schema, *args, **kwargs):
        if "default" in kwargs:
            kwargs["default"] = self._make_multidict(kwargs["default"])
        super(Schema, self).__init__(*args, **kwargs)
        self._schema = dict(schema)  # make a copy

    @handle_undefined_value
    def to_python(self, value):
        fields_received = set(value.keys())
        fields_expected = set(self._schema.keys())
        unknown_fields = fields_received.difference(fields_expected)
        if unknown_fields:
            raise V.SchemaError(
                "Unknown field(s): {!r}".format(sorted(unknown_fields))
            )

        res = {}
        for name, field in self._schema.items():
            if isinstance(field, List):
                v = value.getlist(name, _UNDEFINED)
            else:
                v = value.get(name, _UNDEFINED)

            try:
                v = field.to_python(v)
            except V.SchemaError as e:
                args = list(e.args)
                args[0] = "{}: {}".format(name, args[0])
                e.args = tuple(args)
                raise e
            else:
                res[name] = v

        return self._apply_validators(res)

    @staticmethod
    def _make_multidict(d):
        res = MultiValueDict()
        for k, v in d.items():
            if isinstance(v, list):
                res.setlist(k, v)
            else:
                res[k] = v
        return res


def get_schema_spec(item):
    """Returns a dictionary with the Schema's specification.

    """
    return _get_schema_spec(item, None)


def _get_schema_spec(item, parent=None):
    doc = {
        "description": item.doc,
        "type": item.type_name,
    }
    if item.default is _UNDEFINED:
        doc["required"] = True
    else:
        doc["required"] = False
        doc["default"] = item.default

    if isinstance(item, List):
        doc["extra"] = _get_schema_spec(item._item_type, item)
    elif isinstance(item, Schema):
        doc["extra"] = {k: _get_schema_spec(v, item) for k, v in item._schema.items()}

    if not isinstance(parent, Schema):
        # NOTE: _Type defines "required" and "default" for convenience
        # but they only make sense for items within an Schema (any
        # named container).
        doc.pop("required", None)
        doc.pop("default", None)

    return doc
