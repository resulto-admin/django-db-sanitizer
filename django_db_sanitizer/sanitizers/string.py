import re

from django.utils.crypto import get_random_string

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


class RandomTextSanitizer(BaseSanitizer):

    preserve_punctuation = True

    punctuation_chars = '.,!?;:'

    allowed_chars = 'abcdefghijklmnopqrstuvwxyz' \
                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
                    '0123456789'

    # Get all words of configured fields, and use django crypto
    # get_random_string for each one? Likely super slow but perhaps the only
    # way that'd be safe.

    def sanitize_field_value(self, field_value):
        """Executes the sanitizing operation on a single field and returns
        the result.

        Override this method in concrete Sanitizer classes.

        :param field_value: Value of a field to be sanitized
        :return: Sanitized field value
        """
        # TODO alternative when preserve_punctuation is false
        sanitized_tokens = []
        tokens = re.findall(r"[\w'] + |[" + self.punctuation_chars + "]",
                            field_value)

        for token in tokens:
            if token in self.punctuation_chars:
                sanitized_tokens.append(token)
            else:
                new_token = get_random_string(len(token),
                                              allowed_chars=self.allowed_chars)
                sanitized_tokens.append(new_token)

        return " ".join(sanitized_tokens)
