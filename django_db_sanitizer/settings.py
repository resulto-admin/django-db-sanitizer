from django.conf import settings


DEFAULT_SANITIZER = getattr(settings, 'DEFAULT_SANITIZER', "NullSanitizer")
DEFAULT_UPDATER = getattr(settings, 'DEFAULT_UPDATER', "SimpleUpdater")
