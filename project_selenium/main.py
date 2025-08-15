# main.py

from core.browser_manager import BrowserManager
from pages.login_page import LoginPage



def test_login():
    browser_manager = BrowserManager()
    driver = browser_manager.start_browser()

    try:
        login_page = LoginPage(driver)
        login_page.login()
    finally:
        browser_manager.close_browser(driver)


if __name__ == '__main__':
    test_login()