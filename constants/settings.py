import configparser
import os
from pathlib import Path
from typing import Optional


class Settings:
    """Singleton settings class for application configuration."""
    _instance: Optional['Settings'] = None
    _initialized: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
        self.config = configparser.ConfigParser()
        config_path = Path('config.ini')
        if not config_path.exists():
            config_path = Path('config/config.ini')
        
        if config_path.exists():
            self.config.read(config_path)
        else:
            raise FileNotFoundError(f"Configuration file not found at {config_path}")
        
        Settings._initialized = True

    @property
    def BASE_URL(self) -> str:
        return os.getenv('BASE_URL') or self.config.get('Settings', 'base_url')

    @property
    def BROWSER_TYPE(self) -> str:
        return self.config.get('Settings', 'browser_type', fallback='chromium')

    @property
    def HEADLESS(self) -> bool:
        return self.config.getboolean('Settings', 'headless', fallback=True)

    @property
    def TIMEOUT(self) -> int:
        return self.config.getint('Settings', 'timeout', fallback=30000)

    @property
    def LOG_LEVEL(self) -> str:
        return os.getenv('LOG_LEVEL') or self.config.get('Settings', 'log_level', fallback='INFO')

    @property
    def SCREENSHOT_DIR(self) -> str:
        return self.config.get('Settings', 'screenshot_dir', fallback='screenshots')

    @property
    def REPORT_DIR(self) -> str:
        return self.config.get('Settings', 'report_dir', fallback='reports')
    
    @property
    def USERNAME(self) -> Optional[str]:
        return os.getenv('APP_USERNAME') or self.config.get('Settings', 'username', fallback=None)

    @property
    def PASSWORD(self) -> Optional[str]:
        return os.getenv('APP_PASSWORD') or self.config.get('Settings', 'password', fallback=None)
