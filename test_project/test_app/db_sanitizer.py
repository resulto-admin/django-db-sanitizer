import django_db_sanitizer

from test_app.models import Profile


class CardNumberSanitizer(django_db_sanitizer.NullSanitizer):
    fields_to_sanitize = ("card_number", )


# Register your models here.
django_db_sanitizer.sanitizer_registry.register(Profile, CardNumberSanitizer)
