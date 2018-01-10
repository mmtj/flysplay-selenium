import pytest
from selenium import webdriver


class Base:
    @pytest.fixture(scope="class")
    def browser(self):
        driver = webdriver.Chrome()
        yield driver
        driver.quit()

    @pytest.fixture
    def baseurl(self):
        url = "http://localhost/flyspray"
        return url
