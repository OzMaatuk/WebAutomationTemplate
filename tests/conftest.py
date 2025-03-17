import logging
from configparser import ConfigParser
import pytest
from playwright.sync_api import sync_playwright, BrowserContext, Page
from typing import Generator
from constants.settings import Settings
from pages.login_page import LoginPage
from pages.item_page import ItemPage
from pages.feed_page import FeedPage

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def config() -> ConfigParser:
    config = ConfigParser()
    config.read('pytest.ini')
    return config

@pytest.fixture(scope="session")
def playwright_instance() -> Generator:
    logger.info("Starting Playwright instance...")
    instance = sync_playwright().start()
    yield instance
    logger.info("Stopping Playwright instance...")
    instance.stop()
    logger.info("Playwright instance stopped.")

@pytest.fixture(scope="session")
def playwright_browser(playwright_instance, config: ConfigParser) -> Generator[BrowserContext, None, None]:
    try:
        logger.info("Launching persistent Playwright browser context...")
        headless = Settings().HEADLESS
        browser_context = playwright_instance.webkit.launch(headless=headless)
        logger.info("Persistent browser context launched successfully.")
        yield browser_context
        logger.info("Closing persistent browser context...")
        browser_context.close()
        logger.info("Persistent browser context closed.")
    except Exception as e:
        logger.error(f"Failed to launch persistent browser context: {e}")
        raise

@pytest.fixture(scope="function")
def playwright_page(playwright_browser: BrowserContext, config: ConfigParser) -> Generator[Page, None, None]:
    page = playwright_browser.new_page()
    logger.info("Navigating to test page...")
    page.goto(Settings().BASE_URL)
    logger.info("Test page loaded successfully.")
    yield page
    page.close()

@pytest.fixture
def login_page(page):
    return LoginPage(page)

@pytest.fixture
def search_page(page):
    return FeedPage(page)

@pytest.fixture
def candidate_page(page):
    return ItemPage(page)