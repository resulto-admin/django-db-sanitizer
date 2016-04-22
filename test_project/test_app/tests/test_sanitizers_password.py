from django_db_sanitizer.exceptions import SanitizerValidationException
from django_db_sanitizer.sanitizers.password import PasswordSanitizer

from test_app.models import Profile, User
from test_app.tests.utils import SanitizerTransactionTestCase


class PasswordSanitizerTest(SanitizerTransactionTestCase):
    fixtures = ("profiles",)

    model_class = Profile
    sanitizer_class = PasswordSanitizer

    def test_validate_charfield(self):
        is_valid = self.sanitizer.validate({}, "password", "blah")
        self.assertTrue(is_valid)

    def test_validate_bad_hasher(self):

        class MyPasswordSanitizer(PasswordSanitizer):
            algorithm = "nope.png"
        self.sanitizer = MyPasswordSanitizer(self.model_class)

        with self.assertRaises(SanitizerValidationException):
            self.sanitizer.validate({}, "password", "blah")

    def test_sanitize(self):
        user = User.objects.get(pk=1)
        self.assertFalse(user.check_password("12345"))

        sanitized_value = self.sanitizer.sanitize({}, "password", "blah")
        User.objects.filter(pk=1).update(password=sanitized_value)

        user = User.objects.get(pk=1)
        self.assertTrue(user.check_password("12345"))
