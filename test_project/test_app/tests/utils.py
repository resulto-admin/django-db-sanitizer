from django.core.exceptions import FieldDoesNotExist
from django.test import TransactionTestCase
from django.utils.six import python_2_unicode_compatible


@python_2_unicode_compatible
class SanitizerTransactionTestCase(TransactionTestCase):

    model_class = None
    sanitizer_class = None

    def __str__(self):
        return "{0}".format(self.__class__.__name__)

    def __init__(self, *args, **kwargs):
        if not self.model_class:
            raise Exception("Configure 'model_class' class parameter in {0}."
                            .format(self))
        if not self.sanitizer_class:
            raise Exception("Configure 'sanitizer_class' class parameter in "
                            "{0}.".format(self))

        self.sanitizer = self.sanitizer_class(self.model_class)

        super(SanitizerTransactionTestCase, self).__init__(*args, **kwargs)

    def get_model_field(self, field_name):
        """Returns the Model class field having the given field name.

        :return: Field of the Model class
        """
        try:
            field = self.model_class._meta.get_field(field_name)
            return field
        except FieldDoesNotExist:
            raise Exception("Field {0} does not exist on Model {1}."
                            .format(field_name, self.model_class))
