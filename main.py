"""Main entry point for web automation application."""
import logging
import sys
from pathlib import Path
from dotenv import load_dotenv
from controller.controller import Controller
from constants.settings import Settings
from driver import PlaywrightDriver
from utils.exceptions import AutomationError, ConfigurationError

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)


def setup_directories() -> None:
    """Create necessary directories for logs, screenshots, etc."""
    settings = Settings()
    
    directories = [
        Path('logs'),
        Path(settings.SCREENSHOT_DIR),
        Path(settings.REPORT_DIR),
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Ensured directory exists: {directory}")


def main() -> int:
    """
    Main automation workflow.
    
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    driver = None
    
    try:
        logger.info("Starting automation process...")
        
        # Setup required directories
        setup_directories()
        
        # Load settings
        settings = Settings()
        
        # Validate credentials
        if not settings.USERNAME or not settings.PASSWORD:
            raise ConfigurationError(
                "Username and password must be provided via environment variables "
                "(APP_USERNAME, APP_PASSWORD) or config.ini"
            )
        
        # Initialize driver with context manager support
        with PlaywrightDriver(headless=settings.HEADLESS) as driver:
            # Create controller and run automation
            controller = Controller(driver.page)
            controller.run(settings.USERNAME, settings.PASSWORD)
        
        logger.info("Automation process completed successfully")
        return 0
        
    except ConfigurationError as e:
        logger.error(f"Configuration error: {e}")
        return 1
        
    except AutomationError as e:
        logger.error(f"Automation error: {e}")
        return 1
        
    except KeyboardInterrupt:
        logger.warning("Automation interrupted by user")
        return 130  # Standard exit code for SIGINT
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return 1
        
    finally:
        # Cleanup if driver wasn't used with context manager
        if driver and hasattr(driver, 'close'):
            try:
                driver.close()
            except Exception as e:
                logger.error(f"Error during cleanup: {e}")


if __name__ == "__main__":
    sys.exit(main())