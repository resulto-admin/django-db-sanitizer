from django_db_sanitizer.sanitizers.base import BaseSanitizer


class RandomAddressSanitizer(BaseSanitizer):
    """Sanitizes configured fields in `fields_to_sanitize` by updating them
    with randomized addresses. The addresses generated are nonsensical and
    will not actually represent existing addresses.
    """

    # Some setup/config to split the data generation by element would be nice
    #   Street Number
    #   Street Name
    #   Postal Code
    #   etc...


    def sanitize_field_value(self, field_value):
        """Executes the sanitizing operation on a single field and returns
        the result.

        Override this method in concrete Sanitizer classes.

        :param field_value: Value of a field to be sanitized
        :return: Sanitized field value
        """
        return field_value

    def _generate_street_number(self):
        pass

    def _generate_street_name(self):
        pass
