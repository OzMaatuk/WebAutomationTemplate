from playwright.sync_api import Page
from constants.login_constants import USERNAME_INPUT, PASSWORD_INPUT, LOGIN_BUTTON
import logging
logger = logging.getLogger(__name__)

class LoginPage:
    def __init__(self, page: Page):
        logger.debug("Initiliazing LoginPage")
        self.page = page

    def login(self, username: str, password: str):
        logger.debug("LoginPage.login")
        self.page.fill(USERNAME_INPUT, username)
        self.page.fill(PASSWORD_INPUT, password)
        self.page.click(LOGIN_BUTTON)