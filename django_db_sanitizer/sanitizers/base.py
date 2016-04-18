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
        item_list = self.fetch()
        self.sanitize(item_list)

    def get_queryset(self):
        """Returns a queryset of the Model class using the Sanitizer class'
        configured filters and exclusions for fetching.

        :return: A queryset of rows with filtering rules applied
        :rtype: QuerySet
        """
        qs = self.model_class.objects\
            .filter(**self.filters_for_fetching)\
            .exclude(**self.excludes_for_fetching)
        return qs

    def get_pk_field_name(self):
        """Returns the field name of the Model class' primary key field.

        :return: The PK field name
        :rtype: str
        """
        return self.model_class._meta.pk.name

    def fetch(self):
        """Returns a queryset returning a .values() of the Model's
        primary key field and the sanitizer's `fields_to_sanitize` fields.

        :return: A queryset of all the rows with fields to sanitize
        :rtype: QuerySet
        """
        pk_field = self.get_pk_field_name()
        required_fields = (pk_field, *tuple(f for f in self.fields_to_sanitize
                                            if f != pk_field))

        item_list = self.get_queryset().values(*required_fields)
        return item_list

    def sanitize(self, item_list):
        """Manages the usage of the sanitizer's associated updater.

        :param QuerySet item_list: QuerySet of rows with fields to sanitize
        :return:
        """
        updater = self.updater_class(item_list, self)
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
