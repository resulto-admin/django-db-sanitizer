import logging

from django_db_sanitizer.exceptions import UpdaterException
from django_db_sanitizer.updaters.base import BaseUpdater


logger = logging.getLogger(__name__)


class SingleValuePerFieldUpdater(BaseUpdater):
    """Use this updater to set the same value to all rows of a given field.
    Each field may receive a different value, depending on the sanitizer.

    Note: If using a custom Fetcher class with filters and/or excludes, this
    updater will not update rows not returned by the resulting queryset!
    """

    def update(self):
        """
        Calls `sanitize` on the first row/value for each field, from
        `fields_to_sanitize`, in the queryset and applies the resulting
        sanitized value to all rows of the field.
        """
        update_dict = {}
        try:
            values_row = self.item_list[0]
        except IndexError:
            raise UpdaterException(
                "No items found in {0}'s item_list. Try to review the Fetcher "
                "class' queryset fetching related attributes.".format(self))
        else:
            for field_name in self.fields_to_sanitize:
                field_value = values_row[field_name]
                sanitized_value = self.sanitizer.execute(
                    values_row, field_name, field_value)
                update_dict[field_name] = sanitized_value

            self.fetcher.get_filtered_queryset().update(**update_dict)


class SingleValuePerFieldRowUpdater(BaseUpdater):
    """Use this updater to set a different value to rows of a given field.
    """

    def update(self):
        """
        Calls `sanitize` on each row/value for each field, from
        `fields_to_sanitize`, in the queryset and applies the resulting
        sanitized value to that field.
        """
        for values_row in self.item_list:
            update_dict = {}
            for field_name in self.fields_to_sanitize:
                field_value = values_row[field_name]
                sanitized_value = self.sanitizer.execute(
                    values_row, field_name, field_value)
                update_dict[field_name] = sanitized_value

            pk_value = values_row[self.model_pk_field]
            filter_dict = {self.model_pk_field: pk_value}

            self.fetcher.get_queryset_manager()\
                .filter(**filter_dict)\
                .update(**update_dict)
