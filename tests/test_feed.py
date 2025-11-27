"""Tests for feed page functionality."""

import pytest
from playwright.sync_api import Locator, Page

from constants.settings import Settings
from pages.feed_page import FeedPage


def test_feed_page_initialization(authenticated_page: Page):
    """Test that FeedPage initializes correctly."""
    feed_page = FeedPage(authenticated_page, viewed_my_profile=False)
    assert feed_page.page is not None
    assert feed_page.settings is not None


def test_feed_page_navigation(authenticated_page: Page, settings: Settings):
    """Test navigation to feed page."""
    feed_page = FeedPage(authenticated_page, viewed_my_profile=False)
    assert settings.BASE_URL in feed_page.current_url


def test_iterate_over_items(authenticated_page: Page):
    """Test iterating over feed items."""
    feed_page = FeedPage(authenticated_page, viewed_my_profile=True)

    # Define a simple processor
    def process_item(item: Locator) -> str:
        return item.get_attribute("id") or "no-id"

    # Test with limit
    results = feed_page.iterate_over_items(process_item, limit=5)

    # Verify results
    assert isinstance(results, list)
    # assert len(results) <= 5  # Uncomment when FEED_ITEMS is configured


def test_get_item_count(authenticated_page: Page):
    """Test getting item count from feed."""
    feed_page = FeedPage(authenticated_page, viewed_my_profile=True)
    count = feed_page.get_item_count()

    assert isinstance(count, int)
    assert count >= 0


@pytest.mark.skip(reason="Search functionality not fully implemented")
def test_search_functionality(authenticated_page: Page):
    """Test search functionality."""
    feed_page = FeedPage(authenticated_page, viewed_my_profile=False)
    feed_page.search("test query")
    # Add assertions based on your implementation
