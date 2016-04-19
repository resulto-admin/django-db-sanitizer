import logging

from django.utils.six import python_2_unicode_compatible


logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class BaseFetcher(object):

    queryset_accessor = "objects"

    filters_for_fetching = {}
    excludes_for_fetching = {}

    def __init__(self, model_class, *args, **kwargs):
        self.model_class = model_class
        super(BaseFetcher, self).__init__()

    def __str__(self):
        return "{0}".format(self.__class__.__name__)

    def get_queryset_manager(self):
        """Returns the queryset manager instance of the Model class that will
        be used to fetch the objects to sanitize.

        :return: A queryset manager instance
        :rtype: Manager
        """
        qs = getattr(self.model_class, self.queryset_accessor)
        return qs

    def get_filtered_queryset(self):
        """Returns a filtered queryset of the Model class using the
        configured filters and exclusions for fetching.

        :return: A queryset of rows with filtering rules applied
        :rtype: QuerySet
        """
        qs = self.get_queryset_manager()\
            .filter(**self.filters_for_fetching)\
            .exclude(**self.excludes_for_fetching)
        return qs

    def get_filtered_queryset_values(self, field_names, include_pk_field=True):
        """Returns a filtered queryset of the Model class using the
        configured filters and exclusions for fetching. The returned queryset
        also has

        :param list field_names: List of field names
        :param bool include_pk_field: Whether to include the model's PK field
        :return: A queryset of rows with filtering rules applied
        :rtype: QuerySet
        """
        qs = self.get_filtered_queryset()

        if include_pk_field:
            pk_field = self.get_model_pk_field_name()
            required_fields = (pk_field, *tuple(f for f in field_names
                                                if f != pk_field))
        else:
            required_fields = tuple(f for f in field_names)

        qs = qs.values(*required_fields)
        return qs

    def get_model_class(self):
        """Returns the Model class.

        :return: The Model class
        :rtype: Model
        """
        return self.model_class

    def get_model_pk_field_name(self):
        """Returns the field name of the Model class' primary key field.

        :return: The PK field name
        :rtype: str
        """
        return self.model_class._meta.pk.name
