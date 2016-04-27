from django.conf import settings


DEFAULT_FETCHER = getattr(settings, 'DB_SANITIZER_DEFAULT_FETCHER',
                          "BaseFetcher")

DEFAULT_UPDATER = getattr(settings, 'DB_SANITIZER_DEFAULT_UPDATER',
                          "SingleValuePerFieldRowUpdater")

TEXT_LOCALE = getattr(settings, 'LANGUAGE_CODE', "en-us")
