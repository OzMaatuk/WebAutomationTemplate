"""Utility modules for web automation framework."""

from .exceptions import (
    AutomationError,
    ConfigurationError,
    ElementNotFoundError,
    LoginError,
    NavigationError,
    TimeoutError,
)

__all__ = [
    "AutomationError",
    "LoginError",
    "ElementNotFoundError",
    "NavigationError",
    "TimeoutError",
    "ConfigurationError",
]
