from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from django_db_sanitizer.fetchers import BaseFetcher
from django_db_sanitizer.registry import SanitizerRegistry
from django_db_sanitizer.sanitizers import NullSanitizer
from django_db_sanitizer.updaters import SingleValuePerFieldRowUpdater

from test_app.models import AbstractProfile, Profile


class SanitizerRegistryTest(TestCase):

    def setUp(self):
        self.registry = SanitizerRegistry()

    def test_str(self):
        self.assertEqual(str(self.registry), "SanitizerRegistry")

    def test_register(self):
        self.registry.register(Profile, ["card_number"], NullSanitizer)

        registry_contents = self.registry.get_registry()

        self.assertEqual(list(registry_contents.keys()), [Profile])
        self.assertEqual(len(registry_contents[Profile]), 1)

        worker = registry_contents[Profile][0]

        self.assertEqual(worker.model_class, Profile)
        self.assertEqual(worker.fields_to_sanitize, ["card_number"])
        self.assertEqual(worker.sanitizer_class, NullSanitizer)
        self.assertEqual(worker.updater_class, SingleValuePerFieldRowUpdater)
        self.assertEqual(worker.fetcher_class, BaseFetcher)
        self.assertEqual(worker.registry, self.registry)

    def test_register_abstract_model(self):
        with self.assertRaises(ImproperlyConfigured):
            self.registry.register(AbstractProfile, [], NullSanitizer)

    def test_register_bad_fetcher(self):

        class BadFetcher(object):
            pass

        with self.assertRaises(ImproperlyConfigured):
            self.registry.register(Profile, [], NullSanitizer,
                                   fetcher_class=BadFetcher)

    def test_register_bad_sanitizer(self):

        class BadSanitizer(object):
            pass

        with self.assertRaises(ImproperlyConfigured):
            self.registry.register(Profile, [], BadSanitizer)

    def test_register_bad_updater(self):

        class BadUpdater(object):
            pass

        with self.assertRaises(ImproperlyConfigured):
            self.registry.register(Profile, [], NullSanitizer,
                                   updater_class=BadUpdater)

    def test_register_bad_fields_to_sanitize(self):
        with self.assertRaises(ImproperlyConfigured):
            self.registry.register(Profile, 1, NullSanitizer)

    def test_is_registered(self):
        self.assertFalse(self.registry.is_registered(Profile))
        self.registry.register(Profile, ["card_number"], NullSanitizer)
        self.assertTrue(self.registry.is_registered(Profile))

    def test_optimize_registry(self):
        # TODO
        self.registry.optimize_registry()
