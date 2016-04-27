from django_db_sanitizer.sanitizers.base import BaseSanitizer


class RandomAddressSanitizer(BaseSanitizer):
    """Sanitizes fields by updating them with randomized addresses.
    The addresses generated are nonsensical and will not actually represent
    existing addresses.
    """

    # TODO To be done for a future version

    def sanitize(self, row_object, field_name, field_value):
        """

        :param field_value: Value of a field to be sanitized
        :return: Sanitized field value
        """
        return field_value
