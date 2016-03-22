from django_db_sanitizer.sanitizers.base import BaseSanitizer


class SimplePasswordSanitizer(BaseSanitizer):
    """Sanitizes configured fields in `fields_to_sanitize` by updating them
    to the same password value for all rows.
    """

    # TODO hash function config?

    def execute(self):
        """Overrides BaseSanitizer functionality to simply update all
        given fields to the same password value.
        """
        update_dict = {f: "TODO" for f in self.fields_to_sanitize}

        self.model_class.objects\
            .filter(**self.filters_for_fetching)\
            .exclude(**self.excludes_for_fetching)\
            .update(**update_dict)

