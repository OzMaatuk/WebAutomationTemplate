"""Logging configuration for the application."""
import logging
import sys
from pathlib import Path
from typing import Optional
from constants.settings import Settings


def configure_application_logging(
    log_level: Optional[str] = None,
    log_file: str = 'logs/automation.log',
    logging_format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
) -> None:
    """
    Configure the root logger for the entire application.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file
        logging_format: Log message format
    """
    # Get log level from parameter or settings
    if log_level is None:
        try:
            log_level = Settings().LOG_LEVEL
        except Exception:
            log_level = 'INFO'
    
    # Convert string log level to logging constant
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Get root logger
    logger = logging.getLogger()
    logger.setLevel(numeric_level)
    
    # Clear existing handlers to avoid duplicates
    if logger.handlers:
        for handler in list(logger.handlers):
            logger.removeHandler(handler)
            handler.close()
    
    # Create formatter
    formatter = logging.Formatter(logging_format)
    
    # Ensure log directory exists
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # File handler with rotation support
    try:
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
    except Exception:
        # Fallback to basic file handler
        file_handler = logging.FileHandler(log_file)
    
    file_handler.setLevel(numeric_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    logger.info(f"Logger configured successfully (level: {log_level})")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a module.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


# Initialize the logger with default settings
configure_application_logging()
logger = logging.getLogger(__name__)