"""Login page object with authentication functionality."""
import logging
from playwright.sync_api import Page
from pages.base_page import BasePage
from constants.login_constants import USERNAME_INPUT, PASSWORD_INPUT, LOGIN_BUTTON
from utils.exceptions import LoginError

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """Page object for login functionality."""
    
    def __init__(self, page: Page):
        """Initialize login page."""
        super().__init__(page)
        logger.debug("Initializing LoginPage")
    
    def login(self, username: str, password: str) -> None:
        """
        Perform login with credentials.
        
        Args:
            username: User's username
            password: User's password
            
        Raises:
            LoginError: If login fails
        """
        try:
            logger.info(f"Attempting login for user: {username}")
            self.safe_fill(USERNAME_INPUT, username)
            self.safe_fill(PASSWORD_INPUT, password)
            self.safe_click(LOGIN_BUTTON)
            
            # Wait for navigation after login
            self.wait_for_navigation()
            logger.info("Login successful")
        except Exception as e:
            logger.error(f"Login failed for user {username}: {e}")
            self.take_screenshot("login_failure")
            raise LoginError(f"Login failed: {e}")
    
    def is_logged_in(self) -> bool:
        """Check if user is already logged in."""
        # Override this method based on your site's logged-in indicator
        return not self.is_visible(LOGIN_BUTTON, timeout=2000)