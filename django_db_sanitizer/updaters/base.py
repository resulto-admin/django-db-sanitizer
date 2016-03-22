from django.utils.six import python_2_unicode_compatible


@python_2_unicode_compatible
class BaseUpdater(object):

    def __init__(self, item_set, sanitizer_object):
        self.item_set = item_set
        self.sanitizer = sanitizer_object
        super(BaseUpdater, self).__init__()

    def __str__(self):
        return "{0}.{1}".format(self.sanitizer.__class__.__name__,
                                self.__class__.__name__)

    def execute(self):
        """Orchestrates the execution of the updater class.
        """
        self.update()

    def update(self):
        """Parses self.item_set and saves the sanitized results in the
        database.

        Override this method in concrete Updater classes.
        """
        pass
