"""Pytest configuration and fixtures for web automation tests."""
import logging
from typing import Generator
import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page, Playwright
from constants.settings import Settings
from pages.login_page import LoginPage
from pages.item_page import ItemPage
from pages.feed_page import FeedPage

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def settings() -> Settings:
    """Provide settings instance for tests."""
    return Settings()


@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright, None, None]:
    """Start and stop Playwright instance for test session."""
    logger.info("Starting Playwright instance...")
    instance = sync_playwright().start()
    yield instance
    logger.info("Stopping Playwright instance...")
    instance.stop()
    logger.info("Playwright instance stopped")


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright, settings: Settings) -> Generator[Browser, None, None]:
    """Launch browser for test session."""
    try:
        logger.info("Launching browser...")
        browser = playwright_instance.chromium.launch(
            headless=settings.HEADLESS,
            args=['--disable-blink-features=AutomationControlled']
        )
        logger.info("Browser launched successfully")
        yield browser
        logger.info("Closing browser...")
        browser.close()
        logger.info("Browser closed")
    except Exception as e:
        logger.error(f"Failed to launch browser: {e}")
        raise


@pytest.fixture(scope="function")
def context(browser: Browser) -> Generator[BrowserContext, None, None]:
    """Create new browser context for each test."""
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        ignore_https_errors=True
    )
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext, settings: Settings) -> Generator[Page, None, None]:
    """Create new page for each test."""
    page = context.new_page()
    page.set_default_timeout(settings.TIMEOUT)
    logger.info("Test page created")
    yield page
    page.close()


@pytest.fixture(scope="function")
def authenticated_page(page: Page, settings: Settings) -> Generator[Page, None, None]:
    """Provide authenticated page for tests requiring login."""
    login_page = LoginPage(page)
    
    if not settings.USERNAME or not settings.PASSWORD:
        pytest.skip("Username and password required for authenticated tests")
    
    try:
        page.goto(settings.BASE_URL)
        login_page.login(settings.USERNAME, settings.PASSWORD)
        logger.info("Test page authenticated")
        yield page
    except Exception as e:
        logger.error(f"Authentication failed: {e}")
        pytest.fail(f"Failed to authenticate test page: {e}")


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """Provide LoginPage instance."""
    return LoginPage(page)


@pytest.fixture
def feed_page(page: Page) -> FeedPage:
    """Provide FeedPage instance."""
    return FeedPage(page)


@pytest.fixture
def item_page(page: Page) -> ItemPage:
    """Provide ItemPage instance."""
    return ItemPage(page)


@pytest.fixture(autouse=True)
def screenshot_on_failure(request, page: Page, settings: Settings):
    """Automatically take screenshot on test failure."""
    yield
    
    # Check if test failed (handle cases where rep_call doesn't exist)
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        try:
            from pathlib import Path
            from datetime import datetime
            
            screenshot_dir = Path(settings.SCREENSHOT_DIR)
            screenshot_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = request.node.name
            filename = f"failure_{test_name}_{timestamp}.png"
            filepath = screenshot_dir / filename
            
            page.screenshot(path=str(filepath))
            logger.info(f"Failure screenshot saved: {filepath}")
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {e}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test result for screenshot fixture.
    
    This is a pytest hook that runs after each test phase (setup, call, teardown).
    It stores the test result so the screenshot_on_failure fixture can check if the test failed.
    You don't need to modify this unless you want to change screenshot behavior.
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)