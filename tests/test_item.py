import pytest
from pages.item_page import ItemPage

def test_item(page: ItemPage):
    item_info = page.get_info()
    assert item_info is not None, "Candidate information should not be None"    
    pass