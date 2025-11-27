"""Custom exceptions for web automation framework."""


class AutomationError(Exception):
    """Base exception for automation errors."""

    pass


class LoginError(AutomationError):
    """Raised when login fails."""

    pass


class ElementNotFoundError(AutomationError):
    """Raised when a required element is not found."""

    pass


class NavigationError(AutomationError):
    """Raised when navigation fails."""

    pass


class TimeoutError(AutomationError):
    """Raised when an operation times out."""

    pass


class ConfigurationError(AutomationError):
    """Raised when configuration is invalid or missing."""

    pass
