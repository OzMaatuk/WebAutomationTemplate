from playwright.sync_api import Page
from controller.facade import Facade
import logging
logger = logging.getLogger(__name__)

class Controller:
    def __init__(self, page: Page, api_key: str = None):
        logger.debug("Initiliazing Controller")
        self.page = page
        self.facade = Facade(page)

    def run(self, username: str = None, password: str = None):
        logger.debug("Controller.run")
        self.facade.login(username, password)
        items = self.facade.collect_items(filter=Facade.filter_item, extract=Facade.extract_id, limit=None)
        for item_id in items:
            self.facade.item_action(item_id)