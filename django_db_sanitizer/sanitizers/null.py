from django_db_sanitizer.sanitizers.base import BaseSanitizer


class NullSanitizer(BaseSanitizer):
    """Sanitizes fields by updating them to `None` values in the database.
    """

    def sanitize(self, row_object, field_name, field_value):
        """Simply returns `None` value.
        """
        return None
