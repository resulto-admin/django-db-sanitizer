from random import randint

from django_db_sanitizer.exceptions import SanitizerValidationException
from django_db_sanitizer.sanitizers.base import BaseSanitizer


MIN_MAX_CHECKS = {
    "IntegerField": (-2147483648, 2147483647),
    "BigIntegerField": (-9223372036854775808, 9223372036854775807),
    "PositiveIntegerField": (0, 2147483647),
    "PositiveSmallIntegerField": (0, 32767),
    "SmallIntegerField": (-32768, 32767)
}


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

    def validate(self, row_object, field_name, field_value):
        field = self.get_model_field(field_name)
        field_type = field.get_internal_type()
        try:
            min_value, max_value = MIN_MAX_CHECKS[field_type]
        except KeyError:
            raise SanitizerValidationException(
                "Field {0} is not an Integer type of field."
                .format(field_name))

        if self.lower_boundary < min_value:
            raise SanitizerValidationException(
                "Lower boundary of {0} is lower than field {1}'s minimum "
                "allowed value.".format(self, field_name))
        if self.higher_boundary > max_value:
            raise SanitizerValidationException(
                "Higher boundary of {0} is higher than field {1}'s maximum "
                "allowed value.".format(self, field_name))

        return True

    def sanitize(self, row_object, field_name, field_value):
        """Returns a random integer. The given parameters are ignored.

        :return: Random integer
        :rtype: int
        """
        return randint(self.lower_boundary, self.higher_boundary)
