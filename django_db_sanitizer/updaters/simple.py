import logging

from django_db_sanitizer.updaters.base import BaseUpdater


logger = logging.getLogger(__name__)


class SingleValuePerFieldUpdater(BaseUpdater):
    """Use this updater to set the same value to all rows of a given field as
    returned by the Sanitizer class' `fetch` method.
    Each field may receive a different value, depending on the sanitizer.
    """

    def update(self):
        """
        Calls `sanitize_field_value` on the first row/value for each field
        queryset and applies the resulting sanitized value to all rows of the
        field for all fields in the sanitizer's `fields_to_sanitize`.
        """
        update_dict = {}
        try:
            values_row = self.item_list[0]
        except KeyError:
            logger.warning("No items found in item_list. Try to review the "
                           "Sanitizer's queryset fetching related attributes.")
        else:
            for field_name in self.sanitizer.fields_to_sanitize:
                field_value = values_row[field_name]
                sanitized_value = \
                    self.sanitizer.sanitize_field_value(field_value)
                update_dict[field_name] = sanitized_value

            self.sanitizer.get_queryset().update(**update_dict)


class SingleValuePerFieldRowUpdater(BaseUpdater):
    """Use this updater to set a different value to rows of a given field
    (as returned by the Sanitizer class' `fetch` method).
    """

    def update(self):
        """
        Calls `sanitize_field_value` on each row/value for each field
        queryset and applies the resulting sanitized value to that row for all
        fields in the sanitizer's `fields_to_sanitize`.
        """
        model_class = self.sanitizer.model_class
        pk_field = self.sanitizer.get_pk_field_name()
        for values_row in self.item_list:
            update_dict = {}
            for field_name in self.sanitizer.fields_to_sanitize:
                field_value = values_row[field_name]
                sanitized_value = \
                    self.sanitizer.sanitize_field_value(field_value)
                update_dict[field_name] = sanitized_value

            pk_value = values_row[pk_field]
            filter_dict = {pk_field: pk_value}
            model_class.objects.filter(**filter_dict).update(**update_dict)
