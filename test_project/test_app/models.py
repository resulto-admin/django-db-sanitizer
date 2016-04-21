from django.contrib.auth.models import User
from django.db import models
from django.utils.six import python_2_unicode_compatible

from test_app.constants import MONTHS, DAY_OF_BIRTH


@python_2_unicode_compatible
class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile")
    card_number = models.CharField(max_length=250, null=True, blank=True)
    initials = models.CharField(max_length=4, null=True, blank=True)

    phone = models.CharField(max_length=100, blank=False, default="911")
    mobile_phone = models.CharField(max_length=100, blank=True, default="")

    address = models.CharField(max_length=500, blank=True, default="")
    city = models.CharField(max_length=250, blank=True, default="")
    zip_code = models.CharField(max_length=25, blank=True, default="")
    state = models.CharField(max_length=100, blank=True, default="")
    country = models.CharField(max_length=100, blank=True, default="")

    awesomeness_rank = models.BigIntegerField(blank=True, default=0)
    importance_rank = models.IntegerField(blank=True, default=0)

    number_of_cars = models.PositiveIntegerField(blank=True, default=0)
    number_of_computers = models.PositiveSmallIntegerField(blank=True,
                                                           default=0)

    month_of_birth = models.CharField(
        max_length=3, choices=MONTHS, blank=True, null=True)
    day_of_birth = models.IntegerField(
        choices=DAY_OF_BIRTH, blank=True, null=True)
    year_of_birth = models.SmallIntegerField(blank=True, null=False)
    date_of_birth = models.DateField(blank=True, null=True)

    money_balance = models.DecimalField(
        max_digits=14, decimal_places=2, default=0)

    internal_notes = models.TextField(default="", blank=True)
    admin_notes = models.TextField(default="", blank=True, max_length=500)

    is_subscribed_to_mailing = models.BooleanField(default=True)

    def __str__(self):
        return "{0} - {1}".format(self.user, self.card_number)
