# -*- coding: utf-8 -*-

# $Id:$

"""Validators and validator factories.

A validator is a callable that receives a value, perfoms some check on
it and either returns the value (maybe modified) or raises an
``SchemaError`` exception.

"""

from __future__ import print_function
from __future__ import unicode_literals

import functools


class SchemaError(Exception):
    """Validation error.

    When raising, pass an string describing the error. Don't
    capitalize the sentence and omit the final dot.

       >>> raise SchemaError("not a valid integer")

    """
    pass


def maybe_None(f):
    """Decorates a validator as accepting the value ``None``.

    When writing a validator usually it's advised to check for
    ``None`` values, otherwise bad things will happen:

    .. code-block:: pycon

       >>> from djira.validators import SchemaError
       >>> def is_odd(v):
       ...     if v % 2 == 0:
       ...         raise SchemaError("not odd")
       ...     return v
       ...
       >>> is_odd(3)
       3
       >>> is_odd(4)
       Traceback (most recent call last):
         ...
       djira.validators.SchemaError: not odd
       >>> is_odd(None)
       Traceback (most recent call last):
         ...
       TypeError: unsupported operand type(s) for %: 'NoneType' and 'int'

    This decorator returns a new validator that will handle ``None``
    values safely:

    .. code-block:: pycon

       >>> from djira.validators import maybe_None
       >>> new_is_odd = maybe_None(is_odd)
       >>> new_is_odd(3)
       3
       >>> new_is_odd(4)
       Traceback (most recent call last):
         ...
       djira.validators.SchemaError: not odd
       >>> new_is_odd(None)
       None

    """
    @functools.wraps(f)
    def validator(v):
        if v is None:
            return None
        return f(v)
    return validator


def bounded(min=None, max=None, getter=lambda x: x):
    """Check boundaries.

    This factory returns a validator that checks the boundaries for
    some property of ``value``, the value itself by default:

    .. code-block:: pycon

       >>> from djira.validators import bounded
       >>> validator = bounded(max=10)
       >>> validator(5)
       5
       >>> validator(11)
       Traceback (most recent call last):
         ...
       SchemaError: value too big


    It can check other properties, just specify a ``getter``:

    .. code-block:: pycon

       >>> len_validator = bounded(min=1, max=10, getter=len)
       >>> len_validator("hello")
       'hello'
       >>> len_validator("hello world")
       Traceback (most recent call last):
         ...
       SchemaError: value too big


    The validator can be applied to any type implementing comparison
    methods, not just numbers::

    .. code-block:: pycon

       >>> validator = bounded(min="ab", max="yz")
       >>> validator("abc")
       'abc'
       >>> validator("zz")
       Traceback (most recent call last):
         ...
       djira.validators.SchemaError: value too big


    :param min: minimum value. No minimum by default.

    :param max: maximum value. No maximum by default.

    :param callable getter: callable thar returns the value of the
      property. By default returns the value itself.

    :returns: a validator

    :raises TypeError: if ``getter`` is not callable.

    :raises ValueError: if neither ``min`` nor ``max``

    """

    if not callable(getter):
        raise TypeError("'getter' must be callable")
    if min is None and max is None:
        raise ValueError("must specify 'min' or 'max'")

    def validator(v):
        value = getter(v)
        if min is not None and value < min:
            raise SchemaError("value too small")
        if max is not None and value > max:
            raise SchemaError("value too big")
        return v

    return validator
