from django.core.exceptions import FieldDoesNotExist
from django.test import TestCase, TransactionTestCase


class UpdaterTransactionTestCase(TransactionTestCase):

    model_class = None
    fetcher_class = None
    sanitizer_class = None
    fields_to_sanitize = None
    updater_class = None

    def __init__(self, *args, **kwargs):
        if not self.model_class:
            raise Exception("Configure 'model_class' class parameter in {0}."
                            .format(self))
        if not self.fetcher_class:
            raise Exception("Configure 'fetcher_class' class parameter in "
                            "{0}.".format(self))
        if not self.sanitizer_class:
            raise Exception("Configure 'sanitizer_class' class parameter in "
                            "{0}.".format(self))
        if not self.fields_to_sanitize:
            raise Exception("Configure 'fields_to_sanitize' class parameter "
                            "in {0}.".format(self))
        if not self.updater_class:
            raise Exception("Configure 'updater_class' class parameter in "
                            "{0}.".format(self))

        self.fetcher = self.fetcher_class(self.model_class)
        self.sanitizer = self.sanitizer_class(self.model_class)
        self.updater = self.updater_class(self.fetcher, self.sanitizer,
                                          self.fields_to_sanitize)

        super(UpdaterTransactionTestCase, self).__init__(*args, **kwargs)

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


class FetcherTestCase(TestCase):

    model_class = None
    fetcher_class = None

    def __init__(self, *args, **kwargs):
        if not self.model_class:
            raise Exception("Configure 'model_class' class parameter in {0}."
                            .format(self))
        if not self.fetcher_class:
            raise Exception("Configure 'fetcher_class' class parameter in "
                            "{0}.".format(self))

        self.fetcher = self.fetcher_class(self.model_class)

        super(FetcherTestCase, self).__init__(*args, **kwargs)

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


class SanitizerTestCase(TestCase):

    model_class = None
    sanitizer_class = None

    def __init__(self, *args, **kwargs):
        if not self.model_class:
            raise Exception("Configure 'model_class' class parameter in {0}."
                            .format(self))
        if not self.sanitizer_class:
            raise Exception("Configure 'sanitizer_class' class parameter in "
                            "{0}.".format(self))

        self.sanitizer = self.sanitizer_class(self.model_class)

        super(SanitizerTestCase, self).__init__(*args, **kwargs)

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
