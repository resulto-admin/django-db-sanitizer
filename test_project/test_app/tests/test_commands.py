try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch

from django.core.management import call_command
from django.test import TransactionTestCase

from django_db_sanitizer.fetchers import BaseFetcher
from django_db_sanitizer.registry import SanitizerRegistry
from django_db_sanitizer.sanitizers import NullSanitizer
from django_db_sanitizer.updaters import SingleValuePerFieldUpdater
from django_db_sanitizer.workers import BaseWorker

from test_app.models import Profile


class SanitizeCommandTest(TransactionTestCase):
    fixtures = ("profiles",)

    model_class = Profile
    sanitizer_class = NullSanitizer

    def setUp(self):
        self.registry = SanitizerRegistry()
        self.registry.register(Profile, ["card_number"], NullSanitizer)

        self.worker = BaseWorker(
            Profile, ["card_number"], NullSanitizer,
            SingleValuePerFieldUpdater, BaseFetcher, self.registry)

        self.mock_get_registry = \
            Mock(return_value=self.registry.get_registry())

    def test_sanitize_my_database(self):
        profile1 = Profile.objects.get(pk=1)
        self.assertEqual(profile1.card_number, "000 000 000 001")
        none_count = Profile.objects.filter(card_number=None).count()
        self.assertEqual(none_count, 0)

        with patch('django_db_sanitizer.management.commands.'
                   'sanitize_my_database.sanitizer_registry.get_registry',
                    new=self.mock_get_registry):
            call_command("sanitize_my_database")
            self.assertEqual(self.mock_get_registry.call_count, 1)

        profile1 = Profile.objects.get(pk=1)
        self.assertIsNone(profile1.card_number)
        none_count = Profile.objects.filter(card_number=None).count()
        self.assertEqual(none_count, 10)
