# from optparse import make_option
import time

from django.core.management.base import BaseCommand  # , CommandError

from django_db_sanitizer import sanitizer_registry


class Command(BaseCommand):
    # option_list = BaseCommand.option_list + (
    #     make_option(
    #         "--db-name",
    #         action="store",
    #         dest="db_name",
    #         default="",
    #         help="Name of the database to sanitize."),
    # )

    def handle(self, *args, **options):
        start = time.time()
        # TODO see if specifying the db with the command will work. Maybe not..
        # db_name = options["db_name"]
        # if not db_name:
        #     raise CommandError("--db-name option value must be provided.")

        registry = sanitizer_registry.get_registry()
        for model_class, sanitizer_list in registry.items():
            for sanitizer in sanitizer_list:
                sanitizer.execute()

        stop = time.time()
        print("Took {0:.3f}s".format(stop - start))
