from random import randint

from faker import Faker

from django_db_sanitizer.exceptions import SanitizerValidationException
from django_db_sanitizer.sanitizers.base import BaseSanitizer
from django_db_sanitizer.settings import TEXT_LOCALE


class RandomEmailSanitizer(BaseSanitizer):
    """Sanitizes configured fields in `fields_to_sanitize` by updating them
    with semi-randomized email addresses.

    Will use the domain configured in the sanitizer.
    If no domain is configured, will attempt to reuse any domain found in the
    sanitized value.
    At worst, will generate an email of valid format, with randomized strings
    and ending in `.com`.
    """

    force_domain = None  # xyz.com

    def __init__(self, model_class, *args, **kwargs):
        self.fake = Faker(TEXT_LOCALE)
        super(RandomEmailSanitizer, self).__init__(model_class)

    def validate(self, row_object, field_name, field_value):
        if self.force_domain:
            parts = self.force_domain.split(".")
            if len(parts) == 1:  # No dot(s)?
                raise SanitizerValidationException(
                    "The format of 'force_domain' class parameter value {0} "
                    "appears invalid in {1}.".format(self.force_domain, self))
        return True

    def sanitize(self, row_object, field_name, field_value):
        """Generates a random email string.

        :return: Email address
        :rtype: str
        """
        if self.force_domain:
            new_email = self._get_forced_domain_email()
        else:
            new_email = self._get_field_value_domain_email(field_value)
            if not new_email:
                new_email = self._get_random_email()

        # Add some randomness to the value to avoid problems
        # if the field value must be unique
        if self.is_model_field_unique(field_name):
            new_email = new_email.replace(
                "@", ".{0}.{1}@".format(self.fake.word(),
                                       randint(0, 999999999)))

        return new_email

    def _get_forced_domain_email(self):
        return "{0}@{1}".format(self.fake.user_name(), self.force_domain)

    def _get_field_value_domain_email(self, field_value):
        domain = field_value.split("@")[-1]
        if not domain:
            return None
        else:
            parts = domain.split(".")
            if len(parts) == 1:
                return None

        return "{0}@{1}".format(self.fake.user_name(), domain)

    def _get_random_email(self):
        return self.fake.safe_email()
