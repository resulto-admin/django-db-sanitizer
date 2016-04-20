from django_db_sanitizer.exceptions import SanitizerValidationException
from django_db_sanitizer.sanitizers.base import BaseSanitizer


class NullSanitizer(BaseSanitizer):
    """Sanitizes fields by updating them to `None` values in the database.
    """

    def validate(self, row_object, field_name, field_value):
        field = self.get_model_field(field_name)
        if not field.null:
            raise SanitizerValidationException(
                "{0} can not work on fields whose 'null' attribute is set to "
                "False.".format(self))
        return True

    def sanitize(self, row_object, field_name, field_value):
        """Simply returns `None` value.
        """
        return None
