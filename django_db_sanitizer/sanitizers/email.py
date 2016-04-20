from django_db_sanitizer.sanitizers.base import BaseSanitizer


class RandomEmailSanitizer(BaseSanitizer):
    """Sanitizes configured fields in `fields_to_sanitize` by updating them
    with semi-randomized email addresses.

    Will use the domain configured in the sanitizer.
    If no domain is configured, will attempt to reuse any domain found in the
    sanitized value.
    At worst, will generate an email of valid format, with randomized strings
    and ending in `.com`.
    """

    # Domain config? If None reuse domain found in field_value if possible


    def sanitize_field_value(self, row_object, field_name, field_value):
        """

        :param field_value: Value of a field to be sanitized
        :return: Sanitized email address
        :rtype: str
        """
        return field_value
