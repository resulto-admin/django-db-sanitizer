try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

from django_db_sanitizer.exceptions import (
    SanitizerException, SanitizerValidationException
)
from django_db_sanitizer.sanitizers import BaseSanitizer

from test_app.models import Profile
from test_app.tests.utils import SanitizerTestCase


class BaseSanitizerTest(SanitizerTestCase):

    model_class = Profile
    sanitizer_class = BaseSanitizer

    def test_str(self):
        self.assertEqual(str(self.sanitizer), "BaseSanitizer")

    def test_execute(self):
        sanitized_value = self.sanitizer.execute({}, "some_field", "blah")
        self.assertEqual(sanitized_value, "blah")

    def test_execute_validation_fails(self):
        self.sanitizer.validate = Mock(return_value=False)
        with self.assertRaises(SanitizerValidationException):
            self.sanitizer.execute({}, "some_field", "blah")
        self.sanitizer.validate.assert_called_with({}, "some_field", "blah")

    def test_get_model_field(self):
        field = self.sanitizer.get_model_field("card_number")
        expected_field = self.model_class._meta.get_field("card_number")
        self.assertEqual(field, expected_field)

    def test_get_model_field_does_not_exist(self):
        with self.assertRaises(SanitizerException):
            self.sanitizer.get_model_field("what")

    def test_is_model_field_unique_field_unique(self):
        is_unique = self.sanitizer.is_model_field_unique("mobile_phone")
        self.assertTrue(is_unique)

    def test_is_model_field_unique_field_not_unique(self):
        is_unique = self.sanitizer.is_model_field_unique("card_number")
        self.assertFalse(is_unique)

    def test_validate(self):
        is_valid = self.sanitizer.validate({}, "some_field", "blah")
        self.assertTrue(is_valid)

    def test_sanitize(self):
        sanitized_value = self.sanitizer.sanitize({}, "some_field", "blah")
        self.assertEqual(sanitized_value, "blah")
