import pytest
from selenium import webdriver

from models import LoggedInPage, LoginPage
from config import browser_driver


@pytest.mark.usesfixtures("baseurl")
class Base:
    """Base class for all tests with basic fixtures"""

    @pytest.fixture(scope="class")
    def browser(self):
        driver = None

        if browser_driver == "chrome":
            driver = webdriver.Chrome()
        else:
            driver = webdriver.Firefox()

        yield driver
        driver.quit()

    def logout(self, browser, baseurl):
        page_object = LoggedInPage(browser, baseurl)
        page_object.logout()

    def login(self, browser, baseurl, username, password):
        page_object = LoginPage(browser, baseurl)
        page_object.go_to_url()

        page_object.go_to_login_form()
        page_object.log_in(username, password)

        page_object = LoggedInPage(browser, baseurl)

        assert page_object.is_logged()
