# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from django.db import models

from django_db_sanitizer.exceptions import SanitizerValidationException
from django_db_sanitizer.sanitizers.email import RandomEmailSanitizer

from test_app.models import User
from test_app.tests.utils import SanitizerTestCase


class RandomEmailSanitizerTest(SanitizerTestCase):

    model_class = User
    sanitizer_class = RandomEmailSanitizer

    def _get_domain(self, email):
        return email.split("@")[-1]

    def test_validate_emailfield(self):
        is_valid = self.sanitizer.validate({}, "email", "blah@example.com")
        self.assertTrue(is_valid)

    def test_validate_bad_force_domain(self):

        class MyRandomEmailSanitizer(RandomEmailSanitizer):
            force_domain = "bad"
        self.sanitizer = MyRandomEmailSanitizer(self.model_class)

        with self.assertRaises(SanitizerValidationException):
            self.sanitizer.validate({}, "email", "blah@example.com")

    def test_sanitize_with_force_domain(self):

        class MyRandomEmailSanitizer(RandomEmailSanitizer):
            force_domain = "good.ca"
        self.sanitizer = MyRandomEmailSanitizer(self.model_class)

        sanitized_value = self.sanitizer.sanitize({}, "email",
                                                  "blah@example.com")

        self.assertEqual(sanitized_value.split("@")[-1], "good.ca")
        self.assertNotEqual(sanitized_value.split("@")[0], "blah")
        self.assertEqual(len(sanitized_value.split("@")), 2)

    def test_sanitize_with_value_domain(self):
        sanitized_value = self.sanitizer.sanitize({}, "email",
                                                  "blah@example.com")

        self.assertEqual(sanitized_value.split("@")[-1], "example.com")
        self.assertNotEqual(sanitized_value.split("@")[0], "blah")
        self.assertEqual(len(sanitized_value.split("@")), 2)

    def test_sanitize_random_email_existing_value_bad_format_1(self):
        sanitized_value = self.sanitizer.sanitize({}, "email", "blah")
        self.assertTrue("blah" not in sanitized_value)
        self.assertFalse(bool(re.search(r"(\.\d+@){1}", sanitized_value)))
        self.assertEqual(len(sanitized_value.split("@")), 2)

    def test_sanitize_random_email_existing_value_bad_format_2(self):
        sanitized_value = self.sanitizer.sanitize({}, "email", "blah@")
        self.assertTrue("blah" not in sanitized_value)
        self.assertFalse(bool(re.search(r"(\.\d+@){1}", sanitized_value)))
        self.assertEqual(len(sanitized_value.split("@")), 2)

    def test_sanitize_random_email_field_unique(self):

        class MyUser(User):
            my_email = models.EmailField(blank=True, unique=True)
        self.sanitizer = self.sanitizer_class(MyUser)

        sanitized_value = self.sanitizer.sanitize({}, "my_email", "blah")
        self.assertTrue("blah" not in sanitized_value)
        self.assertTrue(bool(re.search(r"(\.\d+@){1}", sanitized_value)))
        self.assertEqual(len(sanitized_value.split("@")), 2)
