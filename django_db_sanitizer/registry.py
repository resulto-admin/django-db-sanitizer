from collections import defaultdict

from django.core.exceptions import ImproperlyConfigured
from django.utils.six import python_2_unicode_compatible

from django_db_sanitizer import sanitizers, updaters, settings


@python_2_unicode_compatible
class SanitizerRegistry(object):

    def __init__(self):
        self._registry = defaultdict(list)

    def __str__(self):
        return "SanitizerRegistry"

    def register(self, model_class, sanitizer_class=None, updater_class=None,
                 **options):
        """Registers the given Django model with the given sanitizing strategy
        class. The model should be a Model class, not an instance.
        If a sanitizer class isn't given, the default sanitizer as per the
        app's settings will be used. The same goes for the updater class.

        :param model_class: Django model to sanitize
        :param sanitizer_class:
        :param updater_class:
        :param options:
        :raises ImproperlyConfigured:
            if the given model is an abstract model
            if the given strategy class is not a subclass of BaseSanitizer
        """
        if model_class._meta.abstract:
            raise ImproperlyConfigured(
                "The {0} model is abstract, so it cannot be sanitized."
                .format(model_class.__name__))

        if sanitizer_class:
            if not issubclass(sanitizer_class, sanitizers.BaseSanitizer):
                raise ImproperlyConfigured(
                    "The {0} sanitizer is not a subclass of BaseSanitizer."
                    .format(sanitizer_class.__name__))
        else:
            sanitizer_class = getattr(sanitizers, settings.DEFAULT_SANITIZER)

        if updater_class:
            if not issubclass(updater_class, updaters.BaseUpdater):
                raise ImproperlyConfigured(
                    "The {0} updater is not a subclass of BaseUpdater."
                    .format(updater_class.__name__))
        else:
            updater_class = getattr(updaters, settings.DEFAULT_UPDATER)

        # Ignore the registration if the model has been swapped out.
        if not model_class._meta.swapped:
            # Instantiate the sanitizer class to save in the registry
            sanitizer_obj = sanitizer_class(model_class, updater_class, self)
            self._registry[model_class].append(sanitizer_obj)

    def is_registered(self, model_class):
        """Check if a model class is registered with the SanitizerRegistry.
        """
        return model_class in self._registry

    def get_registry(self):
        """Returns the SanitizerRegistry.
        """
        return self._registry


sanitizer_registry = SanitizerRegistry()
