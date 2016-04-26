from django_db_sanitizer.fetchers import BaseFetcher
from django_db_sanitizer.sanitizers import NullSanitizer
from django_db_sanitizer.updaters import BaseUpdater

from test_app.models import Profile
from test_app.tests.utils import UpdaterTransactionTestCase


class BaseUpdaterTest(UpdaterTransactionTestCase):
    fixtures = ("profiles",)

    model_class = Profile
    fetcher_class = BaseFetcher
    sanitizer_class = NullSanitizer
    fields_to_sanitize = ["card_number"]
    updater_class = BaseUpdater

    def test_str(self):
        self.assertEqual(str(self.updater), "BaseUpdater")

    def test_execute(self):
        profile1 = Profile.objects.get(pk=1)
        self.assertEqual(profile1.card_number, "000 000 000 001")

        self.updater.execute()

        profile1 = Profile.objects.get(pk=1)
        # BaseUpdater's update doesn't do anything :-)
        self.assertEqual(profile1.card_number, "000 000 000 001")
