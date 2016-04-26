try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch
from unittest import skipIf

from django.conf import settings

from django_db_sanitizer.fetchers import BaseFetcher
from django_db_sanitizer.sanitizers import ZeroSanitizer
from django_db_sanitizer.updaters import BatchMultiValuePostgresUpdater

from test_app.models import Profile
from test_app.tests.utils import UpdaterTransactionTestCase


POSTGRESQL_ENGINE = "django.db.backends.postgresql_psycopg2"


class CustomBatchMultiValuePostgresUpdater(BatchMultiValuePostgresUpdater):

    update_batch_size = 3


@skipIf(settings.DATABASES["default"]["ENGINE"] != POSTGRESQL_ENGINE,
        "PostgreSQL related tests disabled")
class BatchMultiValuePostgresUpdaterTest(UpdaterTransactionTestCase):
    fixtures = ("profiles",)

    model_class = Profile
    fetcher_class = BaseFetcher
    sanitizer_class = ZeroSanitizer
    fields_to_sanitize = ["importance_rank", "day_of_birth"]
    updater_class = CustomBatchMultiValuePostgresUpdater

    def test_execute(self):
        card_0_count = Profile.objects.filter(importance_rank=0).count()
        day_0_count = Profile.objects.filter(day_of_birth=0).count()
        self.assertEqual(card_0_count, 0)
        self.assertEqual(day_0_count, 0)

        self.updater.execute()

        card_0_count = Profile.objects.filter(importance_rank=0).count()
        day_0_count = Profile.objects.filter(day_of_birth=0).count()
        self.assertEqual(card_0_count, 10)
        self.assertEqual(day_0_count, 10)

    def test_execute_count_batches(self):
        with patch('django_db_sanitizer.updaters.batch.pg_bulk_update',
                    new=Mock()) as mock_pg_bulk_update:
            self.updater.execute()
            # 4 batches * 2 fields
            self.assertEqual(mock_pg_bulk_update.call_count, 8)
