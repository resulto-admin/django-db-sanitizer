import logging

from django.core.exceptions import FieldDoesNotExist
from django.utils.six import python_2_unicode_compatible

from django_db_sanitizer.exceptions import SanitizerException


logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class BaseSanitizer(object):

    def __init__(self, model_class, *args, **kwargs):
        self.model_class = model_class
        super(BaseSanitizer, self).__init__()

    def __str__(self):
        return "{0}".format(self.__class__.__name__)

    def execute(self, row_object, field_name, field_value):
        """Orchestrates the execution of the sanitizer class.

        :param row_object: Values dict of the object containing the field to
            be sanitized
        :param str field_name: Name of the field to be sanitized
        :param field_value: Value of a field to be sanitized
        :return: Sanitized value
        """
        is_valid = self.validate(row_object, field_name, field_value)
        if is_valid:
            return self.sanitize(row_object, field_name, field_value)
        else:
            raise SanitizerException("Validation for {0} failed.".format(self))

    def get_model_field(self, field_name):
        """Returns the Model class field having the given field name.

        :param field_name: The field name
        :return: Field of the Model class
        """
        try:
            field = self.model_class._meta.get_field(field_name)
            return field
        except FieldDoesNotExist:
            raise SanitizerException("Field {0} does not exist on Model {1}."
                                     .format(field_name, self.model_class))

    def is_model_field_unique(self, field_name):
        """Returns the value of the field's 'unique' Django attribute in the
        Model class.

        :param field_name: The field name
        :return: Whether the field has unique=True
        :rtype: bool
        """
        field = self.get_model_field(field_name)
        return field.unique

    def validate(self, row_object, field_name, field_value):
        """Validates the configuration of the sanitizer against the Model class
        and the given parameters to ensure the possibility of returning a
        valid value.

        Override this method in concrete Sanitizer classes when necessary.

        :param row_object: Values dict of the object containing the field to
            be sanitized
        :param str field_name: Name of the field to be sanitized
        :param field_value: Value of a field to be sanitized
        :return: Whether the sanitization process can proceed or not
        :rtype: bool
        """
        return True

    def sanitize(self, row_object, field_name, field_value):
        """Executes a sanitizing operation and returns the result.

        Override this method in concrete Sanitizer classes.

        :param row_object: Values dict of the object containing the field to
            be sanitized
        :param str field_name: Name of the field to be sanitized
        :param field_value: Value of a field to be sanitized
        :return: Sanitized value
        """
        return field_value
