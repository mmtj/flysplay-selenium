#!/usr/bin/env python3

import pytest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

######################
# Page object models #
######################


class Page():
    """Base class of all page objects"""
    def __init__(self, browser, url):
        self.browser = browser
        self.url = url

    def go_to_url(self):
        self.browser.get(self.url)

    def check_element_presence(self, by, identity):
        elem = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((by, identity))
        )

        return elem

    def switch_project(self, project):
        select = Select(self.browser.find_element_by_name("project"))
        select.select_by_visible_text(project)

    def get_project_name(self):
        return self.browser.find_element_by_tag_name("span").text

    def project_is_visible(self, project):
        select = Select(self.browser.find_element_by_name("project"))
        opts = select.options

        text_opts = [option.text for option in opts]

        return any(project in t for t in text_opts)

    def project_not_visible(self, project):
        select = Select(self.browser.find_element_by_name("project"))
        opts = select.options

        text_opts = [option.text for option in opts]

        return not any(project in t for t in text_opts)


class LoginPage(Page):
    """Login page model"""
    def go_to_login_form(self):
        self.browser.find_element_by_id("show_loginbox").click()

    def log_in(self, username, password):
        self.browser.find_element_by_id("lbl_user_name").send_keys(username)
        self.browser.find_element_by_id("lbl_password").send_keys(password + Keys.RETURN)

    def login_failure(self):
        return self.check_element_presence(By.CLASS_NAME, "error")


class LoggedInPage(Page):
    """Pages where user is logged in"""
    def is_logged(self):
        return self.check_element_presence(By.CLASS_NAME, "fa-power-off")

    def logout(self):
        self.browser.find_element_by_class_name("fa-power-off").click()


class ProjectPage(LoggedInPage):
    """Projects page model"""
    def go_to_project_overview_page(self):
        self.browser.find_element_by_link_text("Overview").click()

    def get_project_overview_name(self):
        h2 = self.browser.find_element_by_tag_name("h2")
        a = h2.find_element_by_tag_name("a")

        return a.text


#########
# Tests #
#########


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


class TestSeleniumCase(Base):
    @pytest.mark.parametrize('text', ("ZKS", "public"))
    def test_is_public(self, browser, baseurl, text):
        browser.get(baseurl)

        select = Select(browser.find_element_by_name("project"))
        opts = select.options

        text_opts = [option.text for option in opts]

        assert any(text in t for t in text_opts)


class TestLoginLogout(Base):
    def test_step1_login(self, browser, baseurl):
        page_object = LoginPage(browser, baseurl)
        page_object.go_to_url()

        page_object.go_to_login_form()
        page_object.log_in("admin", "admin123")

        page_object = LoggedInPage(browser, baseurl)

        assert page_object.is_logged()

    def test_step2_logout(self, browser, baseurl):
        page_object = LoggedInPage(browser, baseurl)
        page_object.logout()

    def test_invalid_credentials(self, browser, baseurl):
        page_object = LoginPage(browser, baseurl)

        page_object.go_to_url()

        page_object.go_to_login_form()
        page_object.log_in("us3rname", "passw0rd")

        assert page_object.login_failure()


class TestBrowsePublicProject(Base):
    """Simple test case to browse public projects"""
    @pytest.fixture
    def project(self):
        project = "ZKS public project"
        return project

    def test_step1_goto_page(self, browser, baseurl):
        page_object = Page(browser, baseurl)
        page_object.go_to_url()

    def test_step2_switch_project(self, browser, baseurl, project):
        page_object = Page(browser, baseurl)
        page_object.switch_project(project)

        assert project == page_object.get_project_name()

    def test_step3_project_overview_test(self, browser, baseurl, project):
        page_object = ProjectPage(browser, baseurl)

        page_object.go_to_project_overview_page()

        assert project == page_object.get_project_overview_name()


class TestBrowsePrivateProject(Base):
    """Simple test case to browse private projects"""
    @pytest.fixture
    def project(self):
        project = "ZKS Private project"
        return project

    def test_step1_goto_page(self, browser, baseurl):
        page_object = Page(browser, baseurl)
        page_object.go_to_url()

    def test_step2_try_switch_project(self, browser, baseurl, project):
        page_object = Page(browser, baseurl)

        assert page_object.project_not_visible(project)

    def test_step3_login(self, browser, baseurl):
        page_object = LoginPage(browser, baseurl)
        page_object.go_to_url()

        page_object.go_to_login_form()
        page_object.log_in("admin", "admin123")

        page_object = LoggedInPage(browser, baseurl)

        assert page_object.is_logged()

    def test_step4_switch_project(self, browser, baseurl, project):
        page_object = Page(browser, baseurl)
        page_object.switch_project(project)

        assert project == page_object.get_project_name()

    def test_step5_project_overview_test(self, browser, baseurl, project):
        page_object = ProjectPage(browser, baseurl)

        page_object.go_to_project_overview_page()

        assert project == page_object.get_project_overview_name()

    def test_step6_logout(self, browser, baseurl):
        page_object = LoggedInPage(browser, baseurl)
        page_object.logout()
