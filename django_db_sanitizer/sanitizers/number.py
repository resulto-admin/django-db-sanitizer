from random import randint

from django_db_sanitizer.sanitizers.base import BaseSanitizer


class ZeroSanitizer(BaseSanitizer):
    """Sanitizes configured fields in `fields_to_sanitize` by updating them
    to 0 in the database.
    """

    def execute(self):
        """Overrides BaseSanitizer functionality to simply update all
        given fields to a 0 value.
        """
        update_dict = {f: 0 for f in self.fields_to_sanitize}

        self.model_class.objects\
            .filter(**self.filters_for_fetching)\
            .exclude(**self.excludes_for_fetching)\
            .update(**update_dict)


class RandomIntegerSanitizer(BaseSanitizer):
    """Sanitizes configured fields in `fields_to_sanitize` by updating them
    with a random integer based on the configured boundaries.
    """

    lower_boundary = 0
    higher_boundary = 10000

    def sanitize_field_value(self, field_value):
        """Returns a random integer. The given `field_value` parameter is
        ignored.

        :param field_value: Value of a field to be sanitized
        :return: Random integer
        :rtype: int
        """
        return randint(self.lower_boundary, self.higher_boundary)
