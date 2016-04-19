from django.conf import settings


DEFAULT_FETCHER = getattr(settings, 'DEFAULT_FETCHER',
                          "BaseFetcher")

DEFAULT_UPDATER = getattr(settings, 'DEFAULT_UPDATER',
                          "SingleValuePerFieldRowUpdater")
