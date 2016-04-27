from django.contrib.auth.models import User

from django_db_sanitizer import (
    sanitizer_registry, BaseFetcher, NullSanitizer, RandomTextSanitizer,
    LoremIpsumSanitizer, RandomIntegerSanitizer, PasswordSanitizer,
    RandomEmailSanitizer,
    SingleValuePerFieldUpdater, SingleValuePerFieldRowUpdater,
    BatchMultiValuePostgresUpdater
)

from test_app.models import Profile


# Custom Sanitizer Classes

class MyPasswordSanitizer(PasswordSanitizer):
    password = "helloworld"


class MyCustomFetcher(BaseFetcher):
    excludes_for_fetching = {"username": "admin1"}


# Register your models here.

# -- Simplest Registration examples
# Set a different random text to "internal_notes" per Profile object.
sanitizer_registry.register(Profile, ["internal_notes"], RandomTextSanitizer)
sanitizer_registry.register(Profile, ["admin_notes"], LoremIpsumSanitizer)


# Set 'None' to all rows of field "card_number" in Profile model.
# Specify an updater class optimized for updating all rows to the same value.
sanitizer_registry.register(Profile, ["card_number"], NullSanitizer,
                            SingleValuePerFieldUpdater)


# -- Registration example with custom classes
# Sets every user's password to 'helloworld' except for user 'admin1' whose
# password is left unchanged at password 'test'
sanitizer_registry.register(
    User, ["password"], MyPasswordSanitizer, SingleValuePerFieldUpdater,
    MyCustomFetcher
)

# -- Specifying different Updater classes
# Same value of Awesomeness (int) for all Profiles
sanitizer_registry.register(
    Profile, ["awesomeness_rank"], RandomIntegerSanitizer,
    SingleValuePerFieldUpdater)
# Different value of Importance (int) for all Profiles
sanitizer_registry.register(
    Profile, ["importance_rank"], RandomIntegerSanitizer,
    SingleValuePerFieldRowUpdater)
# Different random email for every User
sanitizer_registry.register(
    User, ["email"], RandomEmailSanitizer, SingleValuePerFieldRowUpdater
)


# TESTING WITH POSTGRES
# -- Testing BatchMultiValuePostgresUpdater updater class with batch size of 3
# (Commented out because the test project uses SQLite3 by default)
# class MyRandomIntegerSanitizer(RandomIntegerSanitizer):
#     lower_boundary = 1
#     higher_boundary = 5
#
#
# class MyPostgresUpdater(BatchMultiValuePostgresUpdater):
#     update_batch_size = 3
#
#
# sanitizer_registry.register(
#     Profile, ("number_of_cars", "number_of_computers"),
#     MyRandomIntegerSanitizer, MyPostgresUpdater)
