"""Page objects for web automation framework."""
from .base_page import BasePage
from .login_page import LoginPage
from .item_page import ItemPage
from .feed_page import FeedPage

__all__ = ['BasePage', 'LoginPage', 'ItemPage', 'FeedPage']