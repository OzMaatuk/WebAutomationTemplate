"""Tests for login functionality."""

import pytest
from playwright.sync_api import Page

from constants.settings import Settings
from pages.login_page import LoginPage
from utils.exceptions import LoginError


def test_login_page_initialization(page: Page):
    """Test that LoginPage initializes correctly."""
    login_page = LoginPage(page)
    assert login_page.page is not None
    assert login_page.settings is not None


def test_login_with_valid_credentials(login_page: LoginPage, settings: Settings):
    """Test login with valid credentials."""
    if not settings.USERNAME or not settings.PASSWORD:
        pytest.skip("Credentials not configured")

    login_page.page.goto(settings.BASE_URL)
    login_page.login(settings.USERNAME, settings.PASSWORD)

    # Verify successful login (customize based on your site)
    # Example assertions:
    # assert "dashboard" in login_page.current_url
    # assert login_page.is_visible("text=Logout")


def test_login_with_invalid_credentials(login_page: LoginPage, settings: Settings):
    """Test login with invalid credentials."""
    login_page.page.goto(settings.BASE_URL)

    with pytest.raises(LoginError):
        login_page.login("invalid_user", "invalid_password")


def test_login_without_credentials(login_page: LoginPage, settings: Settings):
    """Test login without providing credentials."""
    login_page.page.goto(settings.BASE_URL)

    with pytest.raises(Exception):
        login_page.login("", "")
