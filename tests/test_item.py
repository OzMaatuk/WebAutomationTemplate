"""Tests for item page functionality."""

import pytest
from playwright.sync_api import Page

from constants.settings import Settings
from pages.item_page import ItemPage


def test_item_page_initialization(page: Page):
    """Test that ItemPage initializes correctly."""
    item_page = ItemPage(page, item_id="test123")
    assert item_page.page is not None
    assert item_page.item_id == "test123"
    assert item_page.settings is not None


def test_item_page_without_id(page: Page):
    """Test ItemPage initialization without ID."""
    item_page = ItemPage(page)
    assert item_page.page is not None
    assert item_page.item_id is None


@pytest.mark.skip(reason="Requires valid item URL and ITEM_DETAILS selector")
def test_get_item_info(authenticated_page: Page, settings: Settings):
    """Test getting item information."""
    item_page = ItemPage(authenticated_page, item_id="test123")

    # Navigate to a valid item page
    # item_page.navigate_to_item("test123")

    item_info = item_page.get_info()

    assert item_info is not None
    assert isinstance(item_info, dict)
    assert "id" in item_info
    assert "url" in item_info


@pytest.mark.skip(reason="Action functionality not fully implemented")
def test_perform_action(authenticated_page: Page):
    """Test performing action on item."""
    item_page = ItemPage(authenticated_page, item_id="test123")

    # This should not raise an exception
    item_page.perform_action("test message")


def test_navigate_to_item(page: Page, settings: Settings):
    """Test navigation to specific item."""
    item_page = ItemPage(page)

    # Test URL construction
    item_page.navigate_to_item("test123")

    expected_url = f"{settings.BASE_URL}/item/test123"
    assert expected_url in item_page.current_url
