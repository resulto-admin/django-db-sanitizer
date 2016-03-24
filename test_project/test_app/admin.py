from django.contrib import admin

from test_app.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "pk", "user", "card_number", "phone", "money_balance")
    list_display_links = ("pk", "user")
    list_filter = ("is_subscribed_to_mailing", )
    search_fields = ("card_number", )
    raw_id_fields = ("user", )


admin.site.register(Profile, ProfileAdmin)
