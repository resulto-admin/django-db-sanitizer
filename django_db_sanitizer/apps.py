from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SimpleDjangoDbSanitizerConfig(AppConfig):
    """Simple AppConfig which does not do automatic discovery."""
    name = 'django_db_sanitizer'
    verbose_name = _("Django DB Sanitizer")

    def ready(self):
        pass


class DjangoDbSanitizerConfig(SimpleDjangoDbSanitizerConfig):
    """The default AppConfig for db_sanitizer which does autodiscovery."""

    def ready(self):
        super(SimpleDjangoDbSanitizerConfig, self).ready()
        self.module.autodiscover()
