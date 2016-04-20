from random import randint

from django_db_sanitizer.sanitizers.base import BaseSanitizer


class ZeroSanitizer(BaseSanitizer):
    """Sanitizes configured fields by updating them to 0 in the database.
    """

    def sanitize(self, row_object, field_name, field_value):
        """Simply returns 0.

        :return: 0 integer
        :rtype: int
        """
        return 0


class RandomIntegerSanitizer(BaseSanitizer):
    """Sanitizes configured fields in `fields_to_sanitize` by updating them
    with a random integer based on the configured boundaries.
    """

    lower_boundary = 0
    higher_boundary = 10000

    def sanitize(self, row_object, field_name, field_value):
        """Returns a random integer. The given parameters are ignored.

        :return: Random integer
        :rtype: int
        """
        return randint(self.lower_boundary, self.higher_boundary)
