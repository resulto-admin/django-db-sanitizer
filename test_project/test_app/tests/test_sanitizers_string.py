# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from django_db_sanitizer.exceptions import SanitizerValidationException
from django_db_sanitizer.sanitizers.string import (
    EmptyStringSanitizer, FixedFormatSanitizer, LoremIpsumSanitizer,
    RandomTextSanitizer
)

from test_app.models import Profile
from test_app.tests.utils import SanitizerTestCase


class EmptyStringSanitizerTest(SanitizerTestCase):

    model_class = Profile
    sanitizer_class = EmptyStringSanitizer

    def test_validate_charfield(self):
        is_valid = self.sanitizer.validate({}, "card_number", "blah")
        self.assertTrue(is_valid)

    def test_validate_textfield(self):
        is_valid = self.sanitizer.validate({}, "admin_notes", "blah")
        self.assertTrue(is_valid)

    def test_validate_field_blank_is_false(self):
        with self.assertRaises(SanitizerValidationException):
            self.sanitizer.validate({}, "phone", "blah")

    def test_sanitize(self):
        sanitized_value = self.sanitizer.sanitize({}, "admin_notes", "blah")
        self.assertEqual(sanitized_value, '')


class LoremIpsumSanitizerTest(SanitizerTestCase):

    model_class = Profile
    sanitizer_class = LoremIpsumSanitizer

    def test_validate_charfield(self):
        is_valid = self.sanitizer.validate({}, "card_number", "blah")
        self.assertTrue(is_valid)

    def test_validate_textfield(self):
        is_valid = self.sanitizer.validate({}, "admin_notes", "blah")
        self.assertTrue(is_valid)

    def test_validate_field_too_small(self):
        # field max_length is no good
        with self.assertRaises(SanitizerValidationException):
            self.sanitizer.validate({}, "initials", "blah")

    def test_sanitize(self):
        sanitized_value = self.sanitizer.sanitize({}, "admin_notes", "blah")
        self.assertNotEqual(sanitized_value, "blah")

        field = self.get_model_field("admin_notes")
        self.assertTrue(len(sanitized_value) <= field.max_length)


class FixedFormatSanitizerTest(SanitizerTestCase):

    model_class = Profile
    sanitizer_class = FixedFormatSanitizer

    def test_validate_charfield(self):
        is_valid = self.sanitizer.validate({}, "card_number", "blah")
        self.assertTrue(is_valid)

    def test_validate_textfield(self):
        is_valid = self.sanitizer.validate({}, "admin_notes", "blah")
        self.assertTrue(is_valid)

    def test_sanitize(self):
        pass  # TODO


class RandomTextSanitizerTest(SanitizerTestCase):
    fixtures = ("profiles",)

    model_class = Profile
    sanitizer_class = RandomTextSanitizer

    def test_validate_charfield(self):
        is_valid = self.sanitizer.validate({}, "card_number", "blah")
        self.assertTrue(is_valid)

    def test_validate_textfield(self):
        is_valid = self.sanitizer.validate({}, "admin_notes", "blah")
        self.assertTrue(is_valid)

    def test_sanitize_without_value(self):
        profile = Profile.objects.get(pk=7)
        sanitized_value = self.sanitizer.sanitize({}, "internal_notes",
                                                  profile.internal_notes)
        self.assertEqual(sanitized_value, "")

        field = self.get_model_field("admin_notes")
        self.assertTrue(len(sanitized_value) <= field.max_length)

    def test_sanitize_with_value(self):
        profile = Profile.objects.get(pk=10)
        sanitized_value = self.sanitizer.sanitize({}, "internal_notes",
                                                  profile.internal_notes)
        self.assertEqual(len(sanitized_value), len(profile.internal_notes))

        # Punctuation is preserved
        self.assertEqual(sanitized_value[32], ",")
        self.assertEqual(sanitized_value[43], ".")
        self.assertEqual(sanitized_value[-15], ":")
        self.assertEqual(sanitized_value[-1], "!")

        # Capitalization for sentences
        self.assertTrue(sanitized_value[0].istitle())
        self.assertTrue(sanitized_value[45].istitle())

        # None of the original words remain in the sanitized value
        self.assertFalse("Cette personne réside" in sanitized_value)
        self.assertFalse("à Coolcity" in sanitized_value)
        self.assertFalse("Coolstate" in sanitized_value)
        self.assertFalse("Elle est éligible" in sanitized_value)
        self.assertFalse("à la" in sanitized_value)
        self.assertFalse("Coolpromotion" in sanitized_value)
        self.assertFalse("du mois" in sanitized_value)
        self.assertFalse("du champagne" in sanitized_value)

        # No digits in the sanitized value.
        self.assertFalse(bool(re.search(r"[\d]+$", sanitized_value)))
