import logging

from django.utils.six import python_2_unicode_compatible


logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class BaseWorker(object):

    def __init__(self, model_class, fields_to_sanitize, sanitizer_class,
                 updater_class, fetcher_class, registry, *args, **kwargs):
        self.model_class = model_class
        self.fields_to_sanitize = fields_to_sanitize
        self.sanitizer_class = sanitizer_class
        self.updater_class = updater_class
        self.fetcher_class = fetcher_class
        self.registry = registry
        super(BaseWorker, self).__init__()

    def __str__(self):
        return "{0}".format(self.__class__.__name__)

    def execute(self):
        """Orchestrates the sanitization process for the configured model and
        fields.
        """
        fetcher = self.fetcher_class(self.model_class)
        sanitizer = self.sanitizer_class(self.model_class)
        updater = self.updater_class(fetcher, sanitizer,
                                     self.fields_to_sanitize)
        updater.execute()
