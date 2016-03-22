from django.core.exceptions import ImproperlyConfigured
from django.utils.six import python_2_unicode_compatible

from django_db_sanitizer.exceptions import AlreadyRegisteredException
from django_db_sanitizer.sanitizers import BaseSanitizer, NullSanitizer


@python_2_unicode_compatible
class SanitizerRegistry(object):

    def __init__(self):
        self._registry = {}

    def __str__(self):
        return "SanitizerRegistry"

    def register(self, model_class, sanitizer_class=None, **options):
        """Registers the given Django model with the given sanitizing strategy
        class. The model should be a Model class, not an instance.
        If a strategy class isn't given, NullSanitizer (the default sanitizer)
        will be used.

        :param model_class: Django model to sanitize
        :param sanitizer_class:
        :param options:
        :raises ImproperlyConfigured:
            if the given model is an abstract model
            if the given strategy class is not a subclass of BaseSanitizer
        :raises AlreadyRegisteredException:
            if the given model is already registered with a sanitizing strategy
        """
        if model_class._meta.abstract:
            raise ImproperlyConfigured(
                "The {0} model is abstract, so it cannot be sanitized."
                .format(model_class.__name__))

        if sanitizer_class:
            if not issubclass(sanitizer_class, BaseSanitizer):
                raise ImproperlyConfigured(
                    "The {0} sanitizer is not a subclass of BaseSanitizer."
                    .format(sanitizer_class.__name__))
        else:
            sanitizer_class = NullSanitizer

        if model_class in self._registry:
            raise AlreadyRegisteredException(
                "The {0} model is already registered."
                .format(model_class.__name__))

        # Ignore the registration if the model has been swapped out.
        if not model_class._meta.swapped:
            # Instantiate the sanitizer class to save in the registry
            sanitizer_obj = sanitizer_class(model_class, self)
            self._registry[model_class] = sanitizer_obj

    def is_registered(self, model_class):
        """Check if a model class is registered with the SanitizerRegistry.
        """
        return model_class in self._registry

    def get_registry(self):
        """Returns the SanitizerRegistry.
        """
        return self._registry


sanitizer_registry = SanitizerRegistry()
