from django_db_sanitizer.exceptions import SanitizerValidationException
from django_db_sanitizer.sanitizers.number import (
    ZeroSanitizer, RandomIntegerSanitizer
)

from test_app.models import Profile
from test_app.tests.utils import SanitizerTestCase


class ZeroSanitizerTest(SanitizerTestCase):

    model_class = Profile
    sanitizer_class = ZeroSanitizer

    def test_validate_integerfield(self):
        is_valid = self.sanitizer.validate({}, "importance_rank", 1)
        self.assertTrue(is_valid)

    def test_validate_bigintegerfield(self):
        is_valid = self.sanitizer.validate({}, "awesomeness_rank", 1)
        self.assertTrue(is_valid)

    def test_validate_smallintegerfield(self):
        is_valid = self.sanitizer.validate({}, "year_of_birth", 1)
        self.assertTrue(is_valid)

    def test_validate_positiveintegerfield(self):
        is_valid = self.sanitizer.validate({}, "number_of_cars", 1)
        self.assertTrue(is_valid)

    def test_validate_positivesmallintegerfield(self):
        is_valid = self.sanitizer.validate({}, "number_of_computers", 1)
        self.assertTrue(is_valid)

    def test_sanitize(self):
        sanitized_value = self.sanitizer.sanitize({}, "importance_rank", 1)
        self.assertEqual(sanitized_value, 0)


class RandomIntegerSanitizerTest(SanitizerTestCase):

    model_class = Profile
    sanitizer_class = RandomIntegerSanitizer

    def test_validate_integerfield(self):
        is_valid = self.sanitizer.validate({}, "importance_rank", 1)
        self.assertTrue(is_valid)

    def test_validate_bigintegerfield(self):
        is_valid = self.sanitizer.validate({}, "awesomeness_rank", 1)
        self.assertTrue(is_valid)

    def test_validate_smallintegerfield(self):
        is_valid = self.sanitizer.validate({}, "year_of_birth", 1)
        self.assertTrue(is_valid)

    def test_validate_positiveintegerfield(self):
        is_valid = self.sanitizer.validate({}, "number_of_cars", 1)
        self.assertTrue(is_valid)

    def test_validate_positivesmallintegerfield(self):
        is_valid = self.sanitizer.validate({}, "number_of_computers", 1)
        self.assertTrue(is_valid)

    def test_validate_positivesmallintegerfield_bad_lower(self):

        class MyRandomIntegerSanitizer(RandomIntegerSanitizer):
            lower_boundary = -5
        self.sanitizer = MyRandomIntegerSanitizer(self.model_class)

        with self.assertRaises(SanitizerValidationException):
            self.sanitizer.validate({}, "number_of_computers", 1)

    def test_validate_positivesmallintegerfield_bad_higher(self):

        class MyRandomIntegerSanitizer(RandomIntegerSanitizer):
            higher_boundary = 99999999
        self.sanitizer = MyRandomIntegerSanitizer(self.model_class)

        with self.assertRaises(SanitizerValidationException):
            self.sanitizer.validate({}, "number_of_computers", 1)

    def test_validate_wrong_field_type(self):
        with self.assertRaises(SanitizerValidationException):
            self.sanitizer.validate({}, "card_number", "blah")

    def test_sanitize(self):
        sanitized_value = self.sanitizer.sanitize({}, "importance_rank", 1)
        self.assertTrue(sanitized_value in range(0, 10000))
