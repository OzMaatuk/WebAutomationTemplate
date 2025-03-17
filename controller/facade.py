from playwright.sync_api import Page
from constants.settings import Settings
from pages.login_page import LoginPage
from pages.feed_page import FeedPage
from pages.item_page import ItemPage
import logging
logger = logging.getLogger(__name__)

class Facade:
    def __init__(self, page):
        logger.debug("Initiliazing Facade")
        self.page = page

    def login(self, username: str, password: str):
        logger.debug("Facade.login")
        login_page = LoginPage(self.page)
        self.page.goto(Settings().BASE_URL)
        login_page.login(username, password)

    def collect_items(self, filter: function, extract: function, limit: int = None):
        logger.debug("Facade.collect_items")
        feed_page = FeedPage(self.page, viewed_my_profile=True)
        
        def process_item(item):
            filter(item)
            item.click()
            return extract(item)
        
        res = feed_page.iterate_over_items(process_item, limit)
        return res

    def apply_filters(self, filters: dict):
        feed_page = FeedPage(self.page, viewed_my_profile=True)
        # feed_page.search(filters['min_age'])
        # etc...
        pass
    
    def item_action(page: Page, id: str):
        logger.debug("Facade.operate_on_item")
        item_page = ItemPage(page, id)
        item_details = item_page.get_info()
        pass

    def filter_item(item_page: ItemPage, filter_description: str):
        # should use llm to filter items
        return True

    def extract_id(page: Page):
        pass

    def close(self):
        self.context.close()
        self.browser.close()