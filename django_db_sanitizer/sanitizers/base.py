import logging

from django.utils.six import python_2_unicode_compatible


logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class BaseSanitizer(object):

    filter_field_names = ("id",)
    # TODO: Multiple-field primary keys support for filter_field_names
    fields_to_sanitize = ()

    filters_for_fetching = {}
    excludes_for_fetching = {}

    update_batch_size = 1000

    def __init__(self, model_class, registry):
        self.model_class = model_class
        self.registry = registry
        super(BaseSanitizer, self).__init__()

    def __str__(self):
        return "{0}.{1}".format(self.model_class._meta.app_label,
                                self.__class__.__name__)

    def execute(self):
        item_set = self.fetch()

    def fetch(self):
        """Returns a queryset returning a .values_list() of the sanitizer's
        `filter_field_names` and `fields_to_sanitize`.

        :return: A queryset of all the rows with fields to sanitize
        :rtype: QuerySet
        """
        required_fields = \
            tuple(set(self.filter_field_names) | set(self.fields_to_sanitize))

        item_set = self.model_class.objects\
            .filter(**self.filters_for_fetching)\
            .exclude(**self.excludes_for_fetching)\
            .values_list(*required_fields, flat=False)

        return item_set

    def sanitize(self, item_set):
        """

        :param QuerySet item_set: QuerySet of rows with fields to sanitize
        :return:
        """
        pass

    def sanitize_element(self):
        # The operation on one field
        pass


# Note : use iterator while getting rows to prevent memory issues
# Ex:
# foo_set = Foo.objects.all()
# # One database query to test if any rows exist.
# if foo_set.exists():
#     # Another database query to start fetching the rows in batches.
#     for foo in foo_set.iterator():
#         print(foo.bar)



class NullSanitizer(BaseSanitizer):

    def execute(self):
        pass
