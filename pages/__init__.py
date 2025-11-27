"""Page objects for web automation framework."""

from .base_page import BasePage
from .feed_page import FeedPage
from .item_page import ItemPage
from .login_page import LoginPage

__all__ = ["BasePage", "LoginPage", "ItemPage", "FeedPage"]
