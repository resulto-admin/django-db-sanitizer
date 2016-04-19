import re

from django.utils.crypto import get_random_string

from django_db_sanitizer.sanitizers.base import BaseSanitizer


class LoremIpsumSanitizer(BaseSanitizer):

    # TODO Add per-field config of how long the strings should be

    def sanitize(self, row_object, field_name, field_value):
        """

        :param field_value: Value of a field to be sanitized
        :return: Sanitized field value
        """
        return field_value


class FixedFormatSanitizer(BaseSanitizer):

    # Config for expected format

    def sanitize(self, row_object, field_name, field_value):
        """

        :param field_value: Value of a field to be sanitized
        :return: Sanitized field value
        """
        return field_value


class RandomTextSanitizer(BaseSanitizer):
    """This text sanitizer is useful to preserve the general visual appearance
    of a small text or message while obfuscating its actual content.

    It is best used with small paragraphs of text.
    """

    all_punctuation_chars = '.,!?;:'
    sentence_ending_punctuation_chars = ".!?"

    allowed_chars = 'abcdefghijklmnopqrstuvwxyz'

    def sanitize(self, row_object, field_name, field_value):
        """Converts every word found in the text of `field_value` into a
        random string. Preserves punctuation found in the text. Does not
        preserve whitespace other than regular spacing between words.

        :param field_value: Value of the text field to randomize
        :return: Sanitized field value
        """
        sanitized_tokens = []
        format = r"[\w']+|[" + self.all_punctuation_chars + "]"
        tokens = re.findall(format, field_value)

        new_sentence = True
        for token in tokens:
            if token in self.all_punctuation_chars:
                new_token = "".join([sanitized_tokens[-1], token])
                sanitized_tokens[-1] = new_token
                if token in self.sentence_ending_punctuation_chars:
                    new_sentence = True
            else:
                new_token = get_random_string(len(token),
                                              allowed_chars=self.allowed_chars)
                if new_sentence:
                    new_token = new_token.capitalize()
                    new_sentence = False
                sanitized_tokens.append(new_token)

        return " ".join(sanitized_tokens)
