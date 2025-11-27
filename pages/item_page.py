"""Item page object for individual item interactions."""

import logging
from typing import Any, Dict, Optional

from playwright.sync_api import Page

from constants.item_constants import ITEM_DETAILS
from pages.base_page import BasePage
from utils.exceptions import ElementNotFoundError

logger = logging.getLogger(__name__)


class ItemPage(BasePage):
    """Page object for individual item functionality."""

    def __init__(self, page: Page, item_id: Optional[str] = None):
        """
        Initialize item page.

        Args:
            page: Playwright page object
            item_id: Optional item identifier
        """
        super().__init__(page)
        logger.debug(f"Initializing ItemPage with ID: {item_id}")
        self.item_id = item_id

    def get_info(self) -> Dict[str, Any]:
        """
        Extract item information from the page.

        Returns:
            Dictionary containing item details

        Raises:
            ElementNotFoundError: If item details not found
        """
        logger.debug("ItemPage.get_info")

        if not ITEM_DETAILS:
            logger.warning("ITEM_DETAILS selector is empty")
            return {}

        try:
            item_info_text = self.safe_get_text(ITEM_DETAILS)

            # Return structured data
            return {"id": self.item_id, "raw_text": item_info_text, "url": self.current_url}
        except ElementNotFoundError as e:
            logger.error(f"Failed to get item info: {e}")
            self.take_screenshot("item_info_error")
            raise

    def perform_action(self, message: Optional[str] = None) -> None:
        """
        Perform action on the item.

        Args:
            message: Optional message to send/use

        TODO: Implement specific action based on your use case.
        Examples:
            - Send a message: self.safe_fill('#message', message); self.safe_click('#send')
            - Like/favorite: self.safe_click('#like-button')
            - Skip: self.safe_click('#skip-button')
        """
        logger.debug(f"ItemPage.perform_action with message: {message}")

        # TODO: Implement your site-specific action here
        pass

    def navigate_to_item(self, item_id: str) -> None:
        """
        Navigate to specific item by ID.

        Args:
            item_id: Item identifier
        """
        self.item_id = item_id
        url = f"{self.settings.BASE_URL}/item/{item_id}"
        self.navigate_to(url)
