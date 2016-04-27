from django.test import TransactionTestCase

from django_db_sanitizer.fetchers import BaseFetcher
from django_db_sanitizer.registry import SanitizerRegistry
from django_db_sanitizer.sanitizers import NullSanitizer
from django_db_sanitizer.updaters import SingleValuePerFieldUpdater
from django_db_sanitizer.workers import BaseWorker

from test_app.models import Profile


class BaseWorkerTest(TransactionTestCase):
    fixtures = ("profiles",)

    def setUp(self):
        self.registry = SanitizerRegistry()
        self.registry.register(Profile, ["card_number"], NullSanitizer)

        self.worker = BaseWorker(
            Profile, ["card_number"], NullSanitizer,
            SingleValuePerFieldUpdater, BaseFetcher, self.registry)

    def test_str(self):
        self.assertEqual(str(self.worker), "BaseWorker")

    def test_execute(self):
        profile1 = Profile.objects.get(pk=1)
        self.assertEqual(profile1.card_number, "000 000 000 001")

        self.worker.execute()

        profile1 = Profile.objects.get(pk=1)
        self.assertIsNone(profile1.card_number)
