try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

from django_db_sanitizer.fetchers import BaseFetcher

from test_app.models import Profile
from test_app.tests.utils import FetcherTestCase


class BaseFetcherTest(FetcherTestCase):
    fixtures = ("profiles",)

    model_class = Profile
    fetcher_class = BaseFetcher

    def test_str(self):
        self.assertEqual(str(self.fetcher), "BaseFetcher")

    def test_get_queryset_manager(self):
        manager = self.fetcher.get_queryset_manager()
        self.assertEqual(manager, Profile.objects)

    def test_get_filtered_queryset(self):
        queryset = self.fetcher.get_filtered_queryset()
        expected_queryset = Profile.objects.all()
        self.assertEqual(list(queryset), list(expected_queryset))

    def test_get_filtered_queryset_with_filtering(self):

        class MyFilteredFetcher(BaseFetcher):
            filters_for_fetching = {"importance_rank__lte": 5}
            excludes_for_fetching = {"pk": 2}

        self.fetcher = MyFilteredFetcher(self.model_class)
        expected_queryset = Profile.objects.filter(pk__in=[1, 3, 4, 5])

        queryset = self.fetcher.get_filtered_queryset()
        self.assertEqual(list(queryset), list(expected_queryset))

    def test_get_filtered_queryset_values(self):
        queryset = self.fetcher.get_filtered_queryset_values(
            ["card_number"], include_pk_field=True)
        # Actual field name is used instead of Django's "pk" shortcut
        # although it can be requested by adding it to the field_names param
        expected_queryset = Profile.objects.values("id", "card_number")
        self.assertEqual(list(queryset), list(expected_queryset))

    def test_get_filtered_queryset_values_with_pk_keyword_retrieval(self):
        queryset = self.fetcher.get_filtered_queryset_values(
            ["pk", "card_number"], include_pk_field=True)
        expected_queryset = Profile.objects.values("pk", "id", "card_number")
        self.assertEqual(list(queryset), list(expected_queryset))

    def test_get_filtered_queryset_values_no_pk_field(self):
        queryset = self.fetcher.get_filtered_queryset_values(
            ["card_number"], include_pk_field=False)
        expected_queryset = Profile.objects.values("card_number")
        self.assertEqual(list(queryset), list(expected_queryset))

    def test_get_model_class(self):
        model_class = self.fetcher.get_model_class()
        self.assertEqual(model_class, Profile)

    def test_get_model_pk_field_name(self):
        pk_field_name = self.fetcher.get_model_pk_field_name()
        self.assertEqual(pk_field_name, "id")
