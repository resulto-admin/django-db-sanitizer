from django.contrib.auth.models import User

import django_db_sanitizer

from test_app.models import Profile


class CardNumberSanitizer(django_db_sanitizer.NullSanitizer):
    fields_to_sanitize = ("card_number", )


class InternalNotesSanitizer(django_db_sanitizer.RandomTextSanitizer):
    fields_to_sanitize = ("internal_notes", )


class AwesomenessRankSanitizer(django_db_sanitizer.RandomIntegerSanitizer):
    fields_to_sanitize = ("awesomeness_rank", )


class ImportanceRankSanitizer(django_db_sanitizer.RandomIntegerSanitizer):
    fields_to_sanitize = ("importance_rank", )


# Register your models here.

### Registration examples with a sanitizer override
django_db_sanitizer.sanitizer_registry.register(Profile, CardNumberSanitizer)
django_db_sanitizer.sanitizer_registry.register(Profile,
                                                InternalNotesSanitizer)

### Registration example by passing options to a predefined sanitizer
# (Sets everyone's password to 'helloworld' except for user 'admin1')
django_db_sanitizer.sanitizer_registry.register(
    User, django_db_sanitizer.PasswordSanitizer,
    password="helloworld",
    fields_to_sanitize=("password", ),
    excludes_for_fetching={"username": "admin1"}
)

### Using different Updater classes
# Same value of Awesomeness (int) for all Profiles
django_db_sanitizer.sanitizer_registry.register(
    Profile, AwesomenessRankSanitizer,
    django_db_sanitizer.SingleValuePerFieldUpdater)
# Different value of Importance (int) for all Profiles
django_db_sanitizer.sanitizer_registry.register(
    Profile, ImportanceRankSanitizer,
    django_db_sanitizer.SingleValuePerFieldRowUpdater)
