from playwright.sync_api import Page
from constants.feed_constants import FEED_ITEMS, VIEWS_URL_SUFFIX
from constants.settings import Settings
import logging
logger = logging.getLogger(__name__)

class FeedPage:
    def __init__(self, page: Page, viewed_my_profile: bool = True):
        logger.debug("Initiliazing FeedPage")
        self.page = page
        url = Settings().BASE_URL
        if viewed_my_profile: url += VIEWS_URL_SUFFIX
        page.goto(url)

    def iterate_over_items(self, process_item: function, limit: int = None):
        logger.debug("FeedPage.iterate_over_items")
        res = []

        # Locate the search results container
        search_results = self.page.locator(FEED_ITEMS)
        if not search_results.is_visible():
            raise Exception("Search results container not found or not visible.")

        # Find all item elements within the search results
        items = search_results.locator('.item').all()
        logger.info(f"Found {len(items)} items in search results.")

        # Iterate over each item
        for index, item in enumerate(items):
            try:
                res.append(process_item(item))
                if index >= limit:
                    break
            except Exception as e:
                logger.error(f"Error processing item {index}: {e}")


    def search(self, query: str):
        logger.debug("FeedPage.search")
        self.page.fill(self.search_input, query)
        self.page.click(self.search_button)