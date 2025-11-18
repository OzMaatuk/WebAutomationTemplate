"""Utility modules for web automation framework."""
from .exceptions import (
    AutomationError,
    LoginError,
    ElementNotFoundError,
    NavigationError,
    TimeoutError,
    ConfigurationError,
)

__all__ = [
    "AutomationError",
    "LoginError",
    "ElementNotFoundError",
    "NavigationError",
    "TimeoutError",
    "ConfigurationError",
]