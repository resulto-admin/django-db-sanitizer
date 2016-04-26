from django_db_sanitizer.exceptions import UpdaterException
from django_db_sanitizer.fetchers import BaseFetcher
from django_db_sanitizer.sanitizers import (
    NullSanitizer, RandomIntegerSanitizer
)
from django_db_sanitizer.updaters import (
    SingleValuePerFieldUpdater, SingleValuePerFieldRowUpdater
)

from test_app.models import Profile
from test_app.tests.utils import UpdaterTransactionTestCase


class SingleValuePerFieldUpdaterTest(UpdaterTransactionTestCase):
    fixtures = ("profiles",)

    model_class = Profile
    fetcher_class = BaseFetcher
    sanitizer_class = NullSanitizer
    fields_to_sanitize = ["card_number"]
    updater_class = SingleValuePerFieldUpdater

    def test_str(self):
        self.assertEqual(str(self.updater), "SingleValuePerFieldUpdater")

    def test_execute(self):
        profile1 = Profile.objects.get(pk=1)
        self.assertEqual(profile1.card_number, "000 000 000 001")
        none_count = Profile.objects.filter(card_number=None).count()
        self.assertEqual(none_count, 0)

        self.updater.execute()

        profile1 = Profile.objects.get(pk=1)
        self.assertIsNone(profile1.card_number)
        none_count = Profile.objects.filter(card_number=None).count()
        self.assertEqual(none_count, 10)

    def test_execute_no_items_found(self):

        class MyCustomFetcher(BaseFetcher):

            def get_filtered_queryset_values(self, field_names,
                                             include_pk_field=True):
                # Empty queryset
                qs = Profile.objects\
                    .filter(pk__gt=9999999)\
                    .values(*field_names)
                return qs

        self.fetcher = MyCustomFetcher(self.model_class)
        self.updater = self.updater_class(self.fetcher, self.sanitizer,
                                          self.fields_to_sanitize)
        with self.assertRaises(UpdaterException):
            self.updater.execute()


class SingleValuePerFieldRowUpdaterTest(UpdaterTransactionTestCase):
    fixtures = ("profiles",)

    model_class = Profile
    fetcher_class = BaseFetcher
    sanitizer_class = RandomIntegerSanitizer
    fields_to_sanitize = ["importance_rank"]
    updater_class = SingleValuePerFieldRowUpdater

    def test_str(self):
        self.assertEqual(str(self.updater), "SingleValuePerFieldRowUpdater")

    def test_execute(self):
        for i in range(1, 10):
            profile = Profile.objects.get(pk=i)
            self.assertEqual(profile.importance_rank, i)

        self.updater.execute()

        for i in range(1, 10):
            profile = Profile.objects.get(pk=i)
            self.assertNotEqual(profile.importance_rank, i)
