from django.utils.six import python_2_unicode_compatible


@python_2_unicode_compatible
class BaseUpdater(object):

    def __init__(self, fetcher, sanitizer, fields_to_sanitize):
        self.fetcher = fetcher
        self.sanitizer = sanitizer
        self.fields_to_sanitize = fields_to_sanitize
        super(BaseUpdater, self).__init__()

    def __str__(self):
        return "{0}".format(self.__class__.__name__)

    def execute(self):
        """Orchestrates the execution of the updater class.
        """
        # Prepare some attributes
        self.queryset = self.fetcher.get_queryset_manager()
        self.filtered_queryset = self.fetcher.get_filtered_queryset()
        self.item_list = \
            self.fetcher.get_filtered_queryset_values(self.fields_to_sanitize)
        self.model_class = self.fetcher.get_model_class()
        self.model_pk_field = self.fetcher.get_model_pk_field_name()

        self.update()

    def update(self):
        """Parses results from the fetcher, calls upon the sanitizer and saves
        the sanitized results in the database.

        Override this method in concrete Updater classes.
        """
        pass
