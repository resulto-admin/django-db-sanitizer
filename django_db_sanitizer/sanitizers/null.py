from django_db_sanitizer.sanitizers.base import BaseSanitizer


class NullSanitizer(BaseSanitizer):
    """Sanitizes configured fields in `fields_to_sanitize` by updating them
    to `None` values in the database.
    """

    def execute(self):
        """Overrides BaseSanitizer functionality to simply update all
        given fields to a `None` value.
        """
        update_dict = {f: None for f in self.fields_to_sanitize}

        self.model_class.objects\
            .filter(**self.filters_for_fetching)\
            .exclude(**self.excludes_for_fetching)\
            .update(**update_dict)
