from django_db_sanitizer.sanitizers.base import BaseSanitizer


class LoremIpsumSanitizer(BaseSanitizer):

    # TODO Add per-field config of how long the strings should be

    def sanitize_field_value(self, field_value):
        """

        :param field_value: Value of a field to be sanitized
        :return: Sanitized field value
        """
        return field_value


class FixedFormatSanitizer(BaseSanitizer):

    # Config for expected format

    def sanitize_field_value(self, field_value):
        """

        :param field_value: Value of a field to be sanitized
        :return: Sanitized field value
        """
        return field_value
