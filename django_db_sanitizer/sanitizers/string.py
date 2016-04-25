import re

from faker import Faker

from django.utils.crypto import get_random_string

from django_db_sanitizer.exceptions import SanitizerValidationException
from django_db_sanitizer.sanitizers.base import BaseSanitizer
from django_db_sanitizer.settings import TEXT_LOCALE


class EmptyStringSanitizer(BaseSanitizer):
    """Sanitizes fields by updating them to '' values in the database.
    """

    def validate(self, row_object, field_name, field_value):
        field = self.get_model_field(field_name)
        if not field.blank:
            raise SanitizerValidationException(
                "{0} can not work on fields whose 'blank' attribute is set to "
                "False.".format(self))
        return True

    def sanitize(self, row_object, field_name, field_value):
        """Simply returns an empty string '' value.
        """
        return ''


class LoremIpsumSanitizer(BaseSanitizer):
    """Generates Lorem Ipsum text with the possibility of splitting the text
    into paragraphs. It's also possible to specify what set of characters will
    be used to split those paragraphs.

    Note that the field's 'max_length' attribute must be of at least 5
    characters.
    """

    paragraph_quantity = 1
    paragraph_spacer = "\r\n\r\n"

    text_min_length = 5  # Limitation of fake-factory's .text()

    def __init__(self, model_class, *args, **kwargs):
        self.fake = Faker(TEXT_LOCALE)
        super(LoremIpsumSanitizer, self).__init__(model_class)

    def validate(self, row_object, field_name, field_value):
        field = self.get_model_field(field_name)
        if field.max_length < self.text_min_length:
            raise SanitizerValidationException(
                "{0} can not work on text fields with a 'max_length' value "
                "inferior to 5.".format(self))
        return True

    def sanitize(self, row_object, field_name, field_value):
        """Generates Lorem Ipsum text, with the possibility of paragraphs, of
        total character count up to the field's 'max_length' attribute.

        :param field_value: Value of a field to be sanitized
        :return: Sanitized field value
        """
        self._prepare(field_name)

        paragraphs = []
        for i in range(self.paragraph_quantity):
            paragraphs.append(self.fake.text(
                max_nb_chars=self.paragraph_max_length).replace("\n", " "))

        final_text = self.paragraph_spacer.join(paragraphs)
        return final_text

    def _prepare(self, field_name):
        field = self.get_model_field(field_name)
        self.paragraph_max_length = field.max_length // self.paragraph_quantity


class FixedFormatSanitizer(BaseSanitizer):

    # TODO To be done for a future version

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

    Note that this sanitizer will not generate new text for a field that is
    empty.
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
        format = re.compile(r"[\w']+|[" + self.all_punctuation_chars + "]",
                            re.UNICODE)
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
