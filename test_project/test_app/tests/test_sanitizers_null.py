from django_db_sanitizer.exceptions import SanitizerValidationException
from django_db_sanitizer.sanitizers.null import NullSanitizer

from test_app.models import Profile
from test_app.tests.utils import SanitizerTransactionTestCase


class NullSanitizerTest(SanitizerTransactionTestCase):

    model_class = Profile
    sanitizer_class = NullSanitizer

    def test_validate_null_true(self):
        is_valid = self.sanitizer.validate({}, "month_of_birth", 1)
        self.assertTrue(is_valid)

    def test_validate_null_false(self):
        with self.assertRaises(SanitizerValidationException):
            self.sanitizer.validate({}, "year_of_birth", 1)

    def test_sanitize(self):
        sanitized_value = self.sanitizer.sanitize({}, "month_of_birth", 1)
        self.assertEqual(sanitized_value, None)
