from django.contrib.auth.hashers import get_hashers, get_hashers_by_algorithm

from django_db_sanitizer.sanitizers.base import BaseSanitizer
from django_db_sanitizer.exceptions import SanitizerException


class PasswordSanitizer(BaseSanitizer):
    """Sanitizes configured fields in `fields_to_sanitize` by updating them
    to the same password value for all rows. Encrypts said password with the
    configured algorithm. By default, acts the same as Django does by picking
    the first alrogithm in the PASSWORD_HASHERS setting.
    """

    algorithm = "default"
    # By Django's own convention, picks the first password hasher from the
    # PASSWORD_HASHERS setting. To set a specific algorithm, use the values
    # found in the `algorithm` attribute of Django password hasher classes in
    # `django.contrib.auth.hashers`

    password = "12345"

    def sanitize(self, item_set):
        """Overrides BaseSanitizer sanitize to simply update all
        given fields to the password value configured at the class level.
        """
        hasher = self.get_hasher()
        salt = hasher.salt()
        encoded_password = hasher.encode(self.password, salt)

        update_dict = {f: encoded_password for f in self.fields_to_sanitize}
        item_set.update(**update_dict)

    def get_hasher(self):
        if self.algorithm == 'default':
            return get_hashers()[0]

        hashers = get_hashers_by_algorithm()
        try:
            return hashers[self.algorithm]
        except KeyError:
            raise SanitizerException(
                "Password hashing algorithm {0} not found for {1} sanitizer. "
                "Do you have this algorithm configured in your "
                "PASSWORD_HASHERS Django setting?"
                .format(self.algorithm, self))

