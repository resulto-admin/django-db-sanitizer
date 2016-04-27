import time

from django.core.management.base import BaseCommand

from django_db_sanitizer import sanitizer_registry


class Command(BaseCommand):

    def handle(self, *args, **options):
        start = time.time()

        registry = sanitizer_registry.get_registry()
        for model_class, worker_list in registry.items():
            for worker in worker_list:
                worker.execute()

        stop = time.time()
        print("Took {0:.3f}s".format(stop - start))
