import logging
from typing import Optional
from playwright.sync_api import sync_playwright, Page, BrowserContext, Playwright
from constants.settings import Settings

logger = logging.getLogger(__name__)

class PlaywrightDriver:
    """
    Basic Playwright driver operations: initialization, context, and teardown.
    """
    def __init__(self, headless: bool = Settings().HEADLESS, timeout: int = Settings().TIMEOUT, user_data_dir: str = ""):
        logger.info("Initializing PlaywrightDriver parameters...")
        self.headless = headless
        self.timeout = timeout
        self.user_data_dir = user_data_dir
        self._playwright: Optional[Playwright] = None
        self._browser_context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.initialize_driver()
        logger.debug("PlaywrightDriver parameters set.")

    def initialize_driver(self) -> None:
        """Initializes Playwright, browser context, and page."""
        logger.info("Initializing Playwright driver...")
        try:
            self._playwright = sync_playwright().start()
            self._browser_context = self._playwright.chromium.launch_persistent_context(
                user_data_dir=self.user_data_dir,
                headless=self.headless,
                ignore_https_errors=True,
                timeout=self.timeout,
                # Performance optimizations
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                    '--disable-extensions',
                    '--disable-plugins',
                    '--disable-default-apps',
                    '--disable-sync',
                    '--disable-translate',
                    '--disable-background-timer-throttling',
                    '--disable-backgrounding-occluded-windows',
                    '--disable-renderer-backgrounding',
                    '--memory-pressure-off',
                    '--no-sandbox',
                    '--no-first-run',
                    '--no-default-browser-check',
                    '--single-process'
                ],
            )
            self.page = self._browser_context.pages[0] if self._browser_context.pages else self._browser_context.new_page()
            self.page.set_default_timeout(self.timeout)
            logger.info("Playwright browser and page successfully initialized.")
        except Exception as e:
            logger.error(f"Failed to initialize Playwright driver: {e}", exc_info=True)
            self.close()
            raise

    def close(self) -> None:
        """Closes the browser context and stops Playwright."""
        logger.info("Closing Playwright browser context and stopping Playwright...")
        try:
            if self._browser_context:
                self._browser_context.close()
                self._browser_context = None
                self.page = None
            if self._playwright:
                self._playwright.stop()
                self._playwright = None
            logger.debug("Playwright resources closed.")
        except Exception as e:
            logger.error(f"Error while closing Playwright resources: {e}", exc_info=True)

def initialize_driver(headless: bool = True, user_data_dir: str = "") -> Page:
    """
    Legacy initialization function for backward compatibility.
    Returns the page object instead of browser context for direct usage.
    """
    driver = PlaywrightDriver(headless=headless, user_data_dir=user_data_dir)
    return driver.page
