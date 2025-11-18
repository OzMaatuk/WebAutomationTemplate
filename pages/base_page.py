"""Base page class with common functionality for all page objects."""
import logging
from typing import Optional
from pathlib import Path
from playwright.sync_api import Page, Locator, TimeoutError as PlaywrightTimeoutError
from constants.settings import Settings
from utils.exceptions import ElementNotFoundError, TimeoutError

logger = logging.getLogger(__name__)


class BasePage:
    """Base class for all page objects with common functionality."""
    
    def __init__(self, page: Page):
        """Initialize base page with Playwright page object."""
        self.page = page
        self.settings = Settings()
        self.timeout = self.settings.TIMEOUT
    
    def navigate_to(self, url: str) -> None:
        """Navigate to a URL with error handling."""
        try:
            logger.info(f"Navigating to: {url}")
            self.page.goto(url, wait_until="domcontentloaded", timeout=self.timeout)
            logger.debug(f"Successfully navigated to: {url}")
        except PlaywrightTimeoutError as e:
            logger.error(f"Navigation timeout for URL: {url}")
            raise TimeoutError(f"Failed to navigate to {url}: {e}")
        except Exception as e:
            logger.error(f"Navigation failed for URL: {url} - {e}")
            raise
    
    def wait_for_selector(self, selector: str, timeout: Optional[int] = None, state: str = "visible") -> Locator:
        """Wait for element with retry logic."""
        timeout = timeout or self.timeout
        try:
            logger.debug(f"Waiting for selector: {selector}")
            locator = self.page.locator(selector)
            locator.wait_for(state=state, timeout=timeout)
            return locator
        except PlaywrightTimeoutError:
            logger.error(f"Element not found: {selector}")
            raise ElementNotFoundError(f"Element '{selector}' not found within {timeout}ms")
    
    def safe_click(self, selector: str, timeout: Optional[int] = None) -> None:
        """Click element with wait and error handling."""
        try:
            locator = self.wait_for_selector(selector, timeout)
            logger.debug(f"Clicking element: {selector}")
            locator.click()
        except Exception as e:
            logger.error(f"Failed to click element: {selector} - {e}")
            raise
    
    def safe_fill(self, selector: str, value: str, timeout: Optional[int] = None) -> None:
        """Fill input with wait and error handling."""
        try:
            locator = self.wait_for_selector(selector, timeout)
            logger.debug(f"Filling element: {selector}")
            locator.fill(value)
        except Exception as e:
            logger.error(f"Failed to fill element: {selector} - {e}")
            raise
    
    def safe_get_text(self, selector: str, timeout: Optional[int] = None) -> str:
        """Get text content with wait and error handling."""
        try:
            locator = self.wait_for_selector(selector, timeout)
            text = locator.inner_text()
            logger.debug(f"Retrieved text from {selector}: {text[:50]}...")
            return text
        except Exception as e:
            logger.error(f"Failed to get text from element: {selector} - {e}")
            raise
    
    def is_visible(self, selector: str, timeout: int = 5000) -> bool:
        """Check if element is visible without throwing exception."""
        try:
            locator = self.page.locator(selector)
            locator.wait_for(state="visible", timeout=timeout)
            return True
        except PlaywrightTimeoutError:
            return False
    
    def take_screenshot(self, name: str = "screenshot") -> Path:
        """Take screenshot and save to configured directory."""
        screenshot_dir = Path(self.settings.SCREENSHOT_DIR)
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        filepath = screenshot_dir / filename
        
        logger.info(f"Taking screenshot: {filepath}")
        self.page.screenshot(path=str(filepath))
        return filepath
    
    def wait_for_navigation(self, timeout: Optional[int] = None) -> None:
        """Wait for navigation to complete."""
        timeout = timeout or self.timeout
        try:
            self.page.wait_for_load_state("domcontentloaded", timeout=timeout)
            logger.debug("Navigation completed")
        except PlaywrightTimeoutError:
            logger.warning("Navigation wait timed out")
            raise TimeoutError("Navigation did not complete in time")
    
    @property
    def current_url(self) -> str:
        """Get current page URL."""
        return self.page.url
    
    @property
    def title(self) -> str:
        """Get page title."""
        return self.page.title()
