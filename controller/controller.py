"""Main controller for orchestrating automation workflow."""

import logging
from typing import Optional

from playwright.sync_api import Page

from controller.facade import Facade
from utils.exceptions import AutomationError

logger = logging.getLogger(__name__)


class Controller:
    """Main controller for managing automation flow."""

    def __init__(self, page: Page, api_key: Optional[str] = None):
        """
        Initialize controller.

        Args:
            page: Playwright page object
            api_key: Optional API key for external services
        """
        logger.debug("Initializing Controller")
        self.page = page
        self.api_key = api_key
        self.facade = Facade(page)

    def run(self, username: Optional[str] = None, password: Optional[str] = None) -> None:
        """
        Execute the main automation workflow.

        Args:
            username: Login username
            password: Login password

        Raises:
            AutomationError: If workflow fails
        """
        try:
            logger.info("Starting automation workflow")

            # Step 1: Login
            self.facade.login(username, password)

            # Step 2: Collect items
            items = self.facade.collect_items(
                filter_func=Facade.filter_item, extract_func=Facade.extract_id, limit=None
            )

            logger.info(f"Collected {len(items)} items to process")

            # Step 3: Process each item
            for index, item_id in enumerate(items, 1):
                try:
                    logger.info(f"Processing item {index}/{len(items)}: {item_id}")
                    self.facade.item_action(item_id)
                except Exception as e:
                    logger.error(f"Failed to process item {item_id}: {e}")
                    # Continue with next item
                    continue

            logger.info("Automation workflow completed successfully")

        except Exception as e:
            logger.error(f"Automation workflow failed: {e}", exc_info=True)
            raise AutomationError(f"Workflow execution failed: {e}")
