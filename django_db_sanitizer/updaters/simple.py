from django_db_sanitizer.updaters.base import BaseUpdater


class SimpleUpdater(BaseUpdater):
    """Use this updater to set the same value to all rows of a given field.
    Each field may receive a different value, depending on the sanitizer.
    """

    def update(self):
        """

        """
        model_class = self.sanitizer.model_class
        # sanitized_value = self.sanitizer.sanitize_field_value()

        # For each field of item_set,
        # call model_class.objects
        # .filter(**self.filters_for_fetching)\
        # .exclude(**self.excludes_for_fetching)\
        # .update(field_name=sanitized_value)

        # Or for just 1 update call make it roughly equivalent to:

        # update_dict = {f: "call_sanitize_value_here" for f in self.fields_to_sanitize}
        #
        # self.model_class.objects\
        #     .filter(**self.filters_for_fetching)\
        #     .exclude(**self.excludes_for_fetching)\
        #     .update(**update_dict)
