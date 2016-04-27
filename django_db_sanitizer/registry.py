from collections import defaultdict, Iterable

from django.core.exceptions import ImproperlyConfigured
from django.utils.six import python_2_unicode_compatible

from django_db_sanitizer import fetchers, sanitizers, updaters, settings
from django_db_sanitizer.workers import BaseWorker


@python_2_unicode_compatible
class SanitizerRegistry(object):

    def __init__(self):
        self._registry = defaultdict(list)

    def __str__(self):
        return "{0}".format(self.__class__.__name__)

    def register(self, model_class, fields_to_sanitize, sanitizer_class,
                 updater_class=None, fetcher_class=None):
        """Registers the given Django model with the given sanitizing strategy
        class. The model should be a Model class, not an instance.
        If a sanitizer class isn't given, the default sanitizer as per the
        app's settings will be used. The same goes for the updater class.

        :param model_class: Django model to sanitize
        :param fields_to_sanitize:
        :param sanitizer_class:
        :param updater_class:
        :param fetcher_class:
        :raises ImproperlyConfigured:
            if the given model is an abstract model
            if the given fields_to_sanitize is not an Iterable
            if the given sanitizer class is not a subclass of BaseSanitizer
            if the given updater class is not a subclass of BaseUpdater
            if the given fetcher class is not a subclass of BaseFetcher
        """
        if model_class._meta.abstract:
            raise ImproperlyConfigured(
                "The {0} model is abstract, so it cannot be sanitized."
                .format(model_class.__name__))

        if not isinstance(fields_to_sanitize, Iterable):
            raise ImproperlyConfigured(
                "The value of 'fields_to_sanitize' is not an iterable.")

        if not issubclass(sanitizer_class, sanitizers.BaseSanitizer):
            raise ImproperlyConfigured(
                "The {0} sanitizer is not a subclass of BaseSanitizer."
                .format(sanitizer_class.__name__))

        if updater_class:
            if not issubclass(updater_class, updaters.BaseUpdater):
                raise ImproperlyConfigured(
                    "The {0} updater is not a subclass of BaseUpdater."
                    .format(updater_class.__name__))
        else:
            updater_class = getattr(updaters, settings.DEFAULT_UPDATER)

        if fetcher_class:
            if not issubclass(fetcher_class, fetchers.BaseFetcher):
                raise ImproperlyConfigured(
                    "The {0} fetcher is not a subclass of BaseFetcher."
                    .format(fetcher_class.__name__))
        else:
            fetcher_class = getattr(fetchers, settings.DEFAULT_FETCHER)

        # Ignore the registration if the model has been swapped out.
        if not model_class._meta.swapped:
            # Instantiate the worker class to save in the registry
            worker_obj = BaseWorker(
                model_class, fields_to_sanitize, sanitizer_class,
                updater_class, fetcher_class, self)
            self._registry[model_class].append(worker_obj)

    def is_registered(self, model_class):
        """Check if a model class is registered with the SanitizerRegistry.
        """
        return model_class in self._registry

    def get_registry(self):
        """Returns the SanitizerRegistry.
        """
        return self._registry

    def optimize_registry(self):
        """
        """
        # TODO
        pass


sanitizer_registry = SanitizerRegistry()
