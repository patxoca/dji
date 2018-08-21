# -*- coding: utf-8 -*-

# $Id:$

from __future__ import print_function
from __future__ import unicode_literals

from contextlib import contextmanager
import unittest

from .. import validators as V


class _BaseTestCase(unittest.TestCase):

    @contextmanager
    def assertValidationFails(self, regex=None):
        if regex is None:
            manager = self.assertRaises(V.SchemaError)
        else:
            manager = self.assertRaisesRegexp(V.SchemaError, regex)
        with manager:
            yield


class TextMayBeNone(_BaseTestCase):

    def setUp(self):
        def is_even(v):
            if v % 2:
                raise V.SchemaError("not even")
            return v

        self.validator = is_even
        self.new_validator = V.maybe_None(is_even)

    def test_decorated_validator_accepts_None(self):
        # make sure validator(None) errors, just in case
        with self.assertRaises(TypeError):
            self.validator(None)

        self.assertIsNone(self.new_validator(None))

    def test_decorated_validator_behaves_the_same_for_not_None(self):
        # just to be safe
        self.assertEqual(self.validator(2), 2)
        with self.assertRaises(V.SchemaError):
            self.validator(3)

        self.assertEqual(self.new_validator(2), 2)
        with self.assertRaises(V.SchemaError):
            self.new_validator(3)


class TestBounded(_BaseTestCase):

    # factory

    def test_not_callable_getter_raises_TypeError(self):
        with self.assertRaisesRegexp(TypeError, r"'getter' must be callable"):
            V.bounded(min=1, getter=42)

    def test_missing_min_and_max_raises_ValueError(self):
        with self.assertRaisesRegexp(ValueError, r"must specify 'min' or 'max'"):
            V.bounded()

    # validator

    def test_min_value(self):
        validator = V.bounded(min=10)
        print(validator.__doc__)
        validator(10)
        validator(11)
        with self.assertValidationFails(r"value too small"):
            validator(9)

    def test_max_value(self):
        validator = V.bounded(max=10)
        validator(10)
        validator(9)
        with self.assertValidationFails(r"value too big"):
            validator(11)

    def test_both_bounds(self):
        validator = V.bounded(min=5, max=10)
        validator(5)
        validator(7)
        validator(10)
        with self.assertValidationFails(r"value too small"):
            validator(4)
        with self.assertValidationFails(r"value too big"):
            validator(12)

    def test_getter(self):
        validator = V.bounded(max=5, getter=len)
        validator("asdf")
        validator("asdfg")
        with self.assertValidationFails(r"value too big"):
            validator("asdfgh")
