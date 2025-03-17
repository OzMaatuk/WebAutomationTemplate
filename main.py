from controller.controller import Controller
from constants.settings import Settings
from driver import initialize_driver

def main():
    headless: bool = Settings().HEADLESS
    browser = initialize_driver(headless=headless)
    page = browser.pages[0]
    controller = Controller(page)
    controller.run(Settings().USERNAME, Settings().PASSWORD)

if __name__ == "__main__":
    main()