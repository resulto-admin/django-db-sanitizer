from django_db_sanitizer.sanitizers.base import BaseSanitizer


class NullSanitizer(BaseSanitizer):
    """Sanitizes configured fields in `fields_to_sanitize` by updating them
    to `None` values in the database.
    """

    def sanitize(self, item_set):
        """Overrides BaseSanitizer sanitize to simply update all
        given fields to a `None` value.
        """
        update_dict = {f: None for f in self.fields_to_sanitize}
        item_set.update(**update_dict)
