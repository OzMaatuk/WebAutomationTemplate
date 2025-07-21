import logging
import sys
from constants.settings import Settings

def configure_application_logging(
    log_level=Settings().LOG_LEVEL,
    log_file='logs/automation.log',
    logging_format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
):
    """
    Configures the root logger for the entire application.
    """
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Clear existing handlers
    if logger.handlers:
        for handler in list(logger.handlers):
            logger.removeHandler(handler)
            handler.close()

    # Create formatter
    formatter = logging.Formatter(logging_format)

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logger.info("Logger configured successfully.")

# Initialize the logger with default settings
configure_application_logging()
logger = logging.getLogger(__name__)