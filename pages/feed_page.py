"""Feed page object for browsing and filtering items."""

import logging
from typing import Any, Callable, List, Optional

from playwright.sync_api import Locator, Page

from constants.feed_constants import FEED_ITEMS, VIEWS_URL_SUFFIX
from pages.base_page import BasePage
from utils.exceptions import ElementNotFoundError

logger = logging.getLogger(__name__)


class FeedPage(BasePage):
    """Page object for feed/listing functionality."""

    def __init__(self, page: Page, viewed_my_profile: bool = True):
        """
        Initialize feed page.

        Args:
            page: Playwright page object
            viewed_my_profile: Whether to navigate to profile views
        """
        super().__init__(page)
        logger.debug("Initializing FeedPage")

        url = self.settings.BASE_URL
        if viewed_my_profile:
            url += VIEWS_URL_SUFFIX

        self.navigate_to(url)

    def iterate_over_items(
        self, process_item: Callable[[Locator], Any], limit: Optional[int] = None
    ) -> List[Any]:
        """
        Iterate over feed items and process each one.

        Args:
            process_item: Callback function to process each item
            limit: Maximum number of items to process

        Returns:
            List of processed results

        Raises:
            ElementNotFoundError: If feed container not found
        """
        logger.debug("FeedPage.iterate_over_items")
        results = []

        if not FEED_ITEMS:
            logger.warning("FEED_ITEMS selector is empty, skipping iteration")
            return results

        # Wait for and locate the search results container
        try:
            search_results = self.wait_for_selector(FEED_ITEMS)
        except ElementNotFoundError:
            logger.error("Search results container not found")
            self.take_screenshot("feed_not_found")
            raise

        # Find all item elements within the search results
        items = search_results.locator(".item").all()
        logger.info(f"Found {len(items)} items in search results")

        # Determine how many items to process
        items_to_process = min(len(items), limit) if limit else len(items)

        # Iterate over each item
        for index, item in enumerate(items[:items_to_process]):
            try:
                logger.debug(f"Processing item {index + 1}/{items_to_process}")
                result = process_item(item)
                results.append(result)
            except Exception as e:
                logger.error(f"Error processing item {index}: {e}")
                # Continue processing other items
                continue

        logger.info(f"Successfully processed {len(results)} items")
        return results

    def search(self, query: str) -> None:
        """
        Perform search with query.

        Args:
            query: Search query string
        """
        logger.debug(f"FeedPage.search: {query}")
        # Implement search functionality based on your site
        # self.safe_fill(self.search_input, query)
        # self.safe_click(self.search_button)
        logger.warning("Search method not fully implemented")

    def get_item_count(self) -> int:
        """Get total number of items in feed."""
        if not FEED_ITEMS:
            return 0

        try:
            search_results = self.wait_for_selector(FEED_ITEMS, timeout=5000)
            items = search_results.locator(".item").all()
            return len(items)
        except ElementNotFoundError:
            logger.warning("Could not count items - feed not found")
            return 0
