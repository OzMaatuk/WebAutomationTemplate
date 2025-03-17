import configparser
import os


class Settings:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config/config.ini')

    @property
    def BASE_URL(self):
        return self.config.get('Settings', 'base_url')

    @property
    def BROWSER_TYPE(self):
        return self.config.get('Settings', 'browser_type')

    @property
    def HEADLESS(self):
        return self.config.getboolean('Settings', 'headless')

    @property
    def TIMEOUT(self):
        return self.config.getint('Settings', 'timeout')

    @property
    def LOG_LEVEL(self):
        return self.config.get('Settings', 'log_level')

    @property
    def SCREENSHOT_DIR(self):
        return self.config.get('Settings', 'screenshot_dir')

    @property
    def REPORT_DIR(self):
        return self.config.get('Settings', 'report_dir')
    
    @property
    def USERNAME(self):
        return os.getenv('USERNAME') or self.config.get('Settings', 'username')

    @property
    def PASSWORD(self):
        return os.getenv('PASSWORD') or self.config.get('Settings', 'password')
