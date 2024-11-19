class AutomationFrameworkError(Exception):
    """
    Base class for all automation framework errors.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
