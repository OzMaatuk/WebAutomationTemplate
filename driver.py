"""Playwright driver setup and configuration."""

import logging
from pathlib import Path
from typing import Optional

from playwright.sync_api import BrowserContext, Page, Playwright, sync_playwright

from constants.settings import Settings

logger = logging.getLogger(__name__)


class PlaywrightDriver:
    """
    Playwright driver for browser automation.
    Manages browser lifecycle and provides context manager support.
    """

    def __init__(
        self,
        headless: Optional[bool] = None,
        timeout: Optional[int] = None,
        user_data_dir: Optional[str] = None,
    ):
        """
        Initialize Playwright driver.

        Args:
            headless: Run browser in headless mode (default: from settings)
            timeout: Default timeout in milliseconds (default: from settings)
            user_data_dir: Browser profile directory (default: .browser_data)
        """
        logger.info("Initializing PlaywrightDriver parameters...")
        settings = Settings()

        # Use provided values or fall back to settings/defaults
        self.headless = headless if headless is not None else settings.HEADLESS
        self.timeout = timeout if timeout is not None else settings.TIMEOUT
        self.user_data_dir = user_data_dir or str(Path.cwd() / ".browser_data")

        self._playwright: Optional[Playwright] = None
        self._browser_context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

        self.initialize_driver()
        logger.debug("PlaywrightDriver initialized successfully")

    def __enter__(self) -> "PlaywrightDriver":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit with cleanup."""
        self.close()

    def initialize_driver(self) -> None:
        """Initialize Playwright, browser context, and page."""
        logger.info("Initializing Playwright driver...")
        try:
            self._playwright = sync_playwright().start()

            # Create persistent context for session persistence
            self._browser_context = self._playwright.chromium.launch_persistent_context(
                user_data_dir=self.user_data_dir,
                headless=self.headless,
                ignore_https_errors=True,
                timeout=self.timeout,
                viewport={"width": 1920, "height": 1080},
                # Performance and stealth optimizations
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                    "--disable-extensions",
                    "--disable-plugins",
                    "--disable-default-apps",
                    "--disable-sync",
                    "--disable-translate",
                    "--disable-background-timer-throttling",
                    "--disable-backgrounding-occluded-windows",
                    "--disable-renderer-backgrounding",
                    "--memory-pressure-off",
                    "--no-sandbox",
                    "--no-first-run",
                    "--no-default-browser-check",
                ],
            )

            # Get or create page
            if self._browser_context.pages:
                self.page = self._browser_context.pages[0]
            else:
                self.page = self._browser_context.new_page()

            self.page.set_default_timeout(self.timeout)

            logger.info("Playwright browser and page successfully initialized")

        except Exception as e:
            logger.error(f"Failed to initialize Playwright driver: {e}", exc_info=True)
            self.close()
            raise

    def close(self) -> None:
        """Close browser context and stop Playwright."""
        logger.info("Closing Playwright browser context and stopping Playwright...")
        try:
            if self._browser_context:
                self._browser_context.close()
                self._browser_context = None
                self.page = None
                logger.debug("Browser context closed")

            if self._playwright:
                self._playwright.stop()
                self._playwright = None
                logger.debug("Playwright stopped")

            logger.info("Playwright resources closed successfully")

        except Exception as e:
            logger.error(f"Error while closing Playwright resources: {e}", exc_info=True)

    def new_page(self) -> Page:
        """
        Create a new page in the current context.

        Returns:
            New page object
        """
        if not self._browser_context:
            raise RuntimeError("Browser context not initialized")

        page = self._browser_context.new_page()
        page.set_default_timeout(self.timeout)
        return page


def initialize_driver(headless: bool = True, user_data_dir: str = "") -> Page:
    """
    Legacy initialization function for backward compatibility.

    Args:
        headless: Run browser in headless mode
        user_data_dir: Browser profile directory

    Returns:
        Page object for direct usage

    Note:
        Consider using PlaywrightDriver class with context manager instead.
    """
    driver = PlaywrightDriver(headless=headless, user_data_dir=user_data_dir)
    return driver.page
