import logging

from django.utils.six import python_2_unicode_compatible


logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class BaseSanitizer(object):

    fields_to_sanitize = ()

    filters_for_fetching = {}
    excludes_for_fetching = {}

    def __init__(self, model_class, updater_class, registry, *args, **kwargs):
        self.model_class = model_class
        self.updater_class = updater_class
        self.registry = registry
        super(BaseSanitizer, self).__init__()

    def __str__(self):
        return "{0}.{1}".format(self.model_class._meta.app_label,
                                self.__class__.__name__)

    def execute(self):
        """Orchestrates the sanitization process for the configured model and
        fields.
        """
        item_set = self.fetch()
        self.sanitize(item_set)

    def fetch(self):
        """Returns a queryset returning a .values_list() of the Model's
        primary key field and the sanitizer's `fields_to_sanitize` fields.

        :return: A queryset of all the rows with fields to sanitize
        :rtype: QuerySet
        """
        pk_field = self.model_class._meta.pk.name
        required_fields = (pk_field, *tuple(f for f in self.fields_to_sanitize
                                            if f != pk_field))

        item_set = self.model_class.objects\
            .filter(**self.filters_for_fetching)\
            .exclude(**self.excludes_for_fetching)\
            .values_list(*required_fields, flat=False)

        return item_set

    def sanitize(self, item_set):
        """Manages the usage of the sanitizer's associated updater.

        :param QuerySet item_set: QuerySet of rows with fields to sanitize
        :return:
        """
        updater = self.updater_class(item_set, self)
        updater.execute()

    def sanitize_field_value(self, field_value):
        """Executes the sanitizing operation on a single field and returns
        the result.

        Override this method in concrete Sanitizer classes.

        :param field_value: Value of a field to be sanitized
        :return: Sanitized field value
        """
        return field_value



# Note : use iterator while getting rows to prevent memory issues
# Ex:
# foo_set = Foo.objects.all()
# # One database query to test if any rows exist.
# if foo_set.exists():
#     # Another database query to start fetching the rows in batches.
#     for foo in foo_set.iterator():
#         print(foo.bar)
