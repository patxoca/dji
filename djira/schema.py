# -*- coding: utf-8 -*-

# $Id:$

"""The schema allows to specify formally the call interface for an
endpoint.

Example/Motivation: TODO

How missing/undefined values work: TODO


"""

from __future__ import print_function
from __future__ import unicode_literals

from . import validators as V

# marker for missing values
_UNDEFINED = object()


class _Type(object):
    """Base class for schema types.

    """

    type_name = None
    python_type = None

    def __init__(self, default=_UNDEFINED, doc="", validators=()):
        self.default = default
        self.doc = doc
        self._validators = list(validators)  # make a copy

    def to_python(self, value):
        """Converts a value from the request to a python type.

        """
        if value is _UNDEFINED:
            if self.default is _UNDEFINED:
                raise V.SchemaError("missing required value")
            else:
                # NOTE: the default value is assumed to be correct and
                # won't undergo further processing
                return self.default

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

    def to_python(self, value):
        if value is _UNDEFINED:
            if self.default is _UNDEFINED:
                raise V.SchemaError("missing required value")
            else:
                # NOTE: the default value is assumed to be correct and
                # won't undergo further processing
                return self.default

        to_python = self._item_type.to_python
        res = [to_python(i) for i in value]
        return self._apply_validators(res)


class Schema(_Type):
    python_type = dict

    def __init__(self, schema, *args, **kwargs):
        super(Schema, self).__init__(*args, **kwargs)
        self._schema = dict(schema)  # make a copy

    def to_python(self, value):
        if value is _UNDEFINED:
            if self.default is _UNDEFINED:
                raise V.SchemaError("missing required value")
            else:
                # NOTE: the default value is assumed to be correct and
                # won't undergo further processing
                return self.default

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
                mssg, *rest = e.args
                e.args = ("{}: {}".format(name, mssg), *rest)
                raise e
            else:
                res[name] = v

        return self._apply_validators(res)
