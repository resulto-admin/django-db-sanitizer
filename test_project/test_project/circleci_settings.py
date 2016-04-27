def configure(settings):
    settings.DATABASES["default"]["NAME"] = "circle_test"
    settings.DATABASES["default"]["USER"] = "ubuntu"
    settings.DATABASES["default"]["PASSWORD"] = ""
