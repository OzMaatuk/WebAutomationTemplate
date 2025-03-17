from playwright.sync_api import Page
from constants.item_constants import ITEM_DETAILS
import logging
logger = logging.getLogger(__name__)

class ItemPage:
    def __init__(self, page: Page, id: str):
        logger.debug("Initiliazing ItemPage")
        self.page = page
        self.id = id
        
    def get_info(self):
        logger.debug("ItemPage.get_info")
        profile_info = self.page.locator(ITEM_DETAILS).inner_text()
        return profile_info
    
    def action(self, message: str):
        logger.debug("ItemPage.action")
        pass