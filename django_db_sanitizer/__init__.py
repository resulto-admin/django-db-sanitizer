from django.utils.module_loading import autodiscover_modules

from django_db_sanitizer.registry import SanitizerRegistry, sanitizer_registry
from django_db_sanitizer.sanitizers import (
    RandomAddressSanitizer, RandomEmailSanitizer, NullSanitizer, ZeroSanitizer,
    RandomIntegerSanitizer, PasswordSanitizer, FixedFormatSanitizer,
    LoremIpsumSanitizer, RandomTextSanitizer
)
from django_db_sanitizer.updaters import (
    SingleValuePerFieldUpdater, SingleValuePerFieldRowUpdater,
    BatchMultiValuePostgresUpdater
)


__all__ = [
    "register", "RandomAddressSanitizer", "RandomEmailSanitizer",
    "NullSanitizer", "ZeroSanitizer", "RandomIntegerSanitizer",
    "PasswordSanitizer", "FixedFormatSanitizer", "LoremIpsumSanitizer",
    "RandomTextSanitizer",
    "SingleValuePerFieldUpdater", "SingleValuePerFieldRowUpdater",
    "BatchMultiValuePostgresUpdater",
    "autodiscover",
]


def autodiscover():
    autodiscover_modules('db_sanitizer', register_to=sanitizer_registry)


default_app_config = 'django_db_sanitizer.apps.DjangoDbSanitizerConfig'
