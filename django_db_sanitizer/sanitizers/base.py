import logging

from django.utils.six import python_2_unicode_compatible


logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class BaseSanitizer(object):

    def __init__(self, *args, **kwargs):
        super(BaseSanitizer, self).__init__()

    def __str__(self):
        return "{0}".format(self.__class__.__name__)

    def sanitize(self, row_object, field_name, field_value):
        """Executes a sanitizing operation and returns the result.

        Override this method in concrete Sanitizer classes.

        :param row_object:
        :param field_value: Value of a field to be sanitized
        :return: Sanitized value
        """
        return field_value
