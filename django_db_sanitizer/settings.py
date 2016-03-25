from django.conf import settings


DEFAULT_UPDATER = getattr(settings, 'DEFAULT_UPDATER', "SimpleUpdater")
