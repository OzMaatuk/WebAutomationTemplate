import pytest
from pages.login_page import LoginPage

def test_login(login_page: LoginPage):
    """
    Tests the login functionality.
    """
    username = "testuser"
    password = "testpassword"
    
    login_page.login(username, password)
    
    # Add assertions to verify successful login
    assert login_page.page.url == Settings().BASE_URL + "/dashboard"  # Example assertion
    assert login_page.page.is_visible("text=Logout")  # Example assertion for logout button visibility