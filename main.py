import logging
from controller.controller import Controller
from constants.settings import Settings
from driver import PlaywrightDriver

logger = logging.getLogger(__name__)

def main():
    try:
        logger.info("Starting automation process...")
        driver = PlaywrightDriver(headless=Settings().HEADLESS)
        controller = Controller(driver.page)
        controller.run(Settings().USERNAME, Settings().PASSWORD)
    except Exception as e:
        logger.error(f"Automation process failed: {e}", exc_info=True)
        raise
    finally:
        if 'driver' in locals():
            driver.close()
        logger.info("Automation process completed.")

if __name__ == "__main__":
    main()