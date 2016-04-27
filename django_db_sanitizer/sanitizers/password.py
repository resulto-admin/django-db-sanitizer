from django.contrib.auth.hashers import (
    get_hashers, get_hashers_by_algorithm, make_password
)

from django_db_sanitizer.sanitizers.base import BaseSanitizer
from django_db_sanitizer.exceptions import SanitizerValidationException


class PasswordSanitizer(BaseSanitizer):
    """Sanitizes configured fields in `fields_to_sanitize` by updating them
    to the same password value for all rows. Encrypts said password with the
    configured algorithm.

    By default, acts the same as Django does by picking the first alrogithm in
    the PASSWORD_HASHERS setting (uses 'make_password' from Django codebase).
    """

    algorithm = "default"
    # By Django's own convention, picks the first password hasher from the
    # PASSWORD_HASHERS setting. To set a specific algorithm, use the values
    # found in the `algorithm` attribute of Django password hasher classes in
    # `django.contrib.auth.hashers`

    password = "12345"

    def validate(self, row_object, field_name, field_value):
        try:
            self.get_hasher()
        except KeyError:
            raise SanitizerValidationException(
                "Password hashing algorithm {0} not found for {1} sanitizer. "
                "Do you have this algorithm configured in your "
                "PASSWORD_HASHERS Django setting?"
                .format(self.algorithm, self))

        return True

    def sanitize(self, row_object, field_name, field_value):
        """Returns an encoded password using Django's 'make_password'
        """
        return make_password(self.password, hasher=self.algorithm)

    def get_hasher(self):
        if self.algorithm == 'default':
            return get_hashers()[0]
        hashers = get_hashers_by_algorithm()
        return hashers[self.algorithm]
