class DbSanitizerException(Exception):
    """Base Exception class for the app.
    """
    pass


# Exception classes used in registry

class RegistryException(DbSanitizerException):
    pass


# Exception classes used for all sanitizers
