import pytest
from selenium.webdriver.common.by import By

from base import Base
from models import Page, LoginPage, LoggedInPage, AdministrationPage, ProjectPage

"""
incremental => if one step fails, other fails automatically as xfailed
xfailed == expected fail
"""
@pytest.mark.incremental
class TestCreateUsers(Base):
    """Create new users with different roles"""

    testusersdata = [
                    ("developer", "passw0rd", "Developers"),
                    ("reporter", "report3r", "Reporters")
                    ]

    def test_step1_login_as_admin(self, browser, baseurl):
        page_object = LoginPage(browser, baseurl)
        page_object.go_to_url()

        page_object.go_to_login_form()
        page_object.log_in("admin", "admin123")

        page_object = LoggedInPage(browser, baseurl)

        assert page_object.is_logged()

    def test_step2_go_to_administration(self, browser, baseurl):
        page_object = LoggedInPage(browser, baseurl)
        page_object.go_to_site_admin()

        assert page_object.get_section_heading().text == "Administrator's Toolbox :: Preferences"

    @pytest.mark.parametrize("username,password,role", testusersdata)
    def test_step3_add_new_user(self, browser, baseurl, username, password, role):
        page_object = AdministrationPage(browser, baseurl)
        page_object.users_and_groups()

        button = browser.find_element_by_link_text("Register New User")
        assert button.text == "Register New User"

        button.click()
        assert page_object.get_section_heading().text == "Admin Toolbox :: All Projects : Register New User"

        page_object.fill_new_user_form(username, password, role)
        page_object.submit_new_user_form()

        popup = browser.find_element_by_class_name("success")
        assert popup.text == "New User Account has been created."

    def test_step4_logout(self, browser, baseurl):
        page_object = LoggedInPage(browser, baseurl)
        page_object.logout()


class TestCreateUserWhichExists(Base):
    """Test if adding new user with existing username fails"""
    def test_step1_login_as_admin(self, browser, baseurl):
        page_object = LoginPage(browser, baseurl)
        page_object.go_to_url()

        page_object.go_to_login_form()
        page_object.log_in("admin", "admin123")

        page_object = LoggedInPage(browser, baseurl)

        assert page_object.is_logged()

    def test_step2_go_to_administration(self, browser, baseurl):
        page_object = LoggedInPage(browser, baseurl)
        page_object.go_to_site_admin()

        assert page_object.get_section_heading().text == "Administrator's Toolbox :: Preferences"

    @pytest.mark.parametrize("username,password,role", [("reporter", "password", "Reporters")])
    def test_step3_dont_add_existing_user(self, browser, baseurl, username, password, role):
        page_object = AdministrationPage(browser, baseurl)
        page_object.users_and_groups()

        button = browser.find_element_by_link_text("Register New User")
        assert button.text == "Register New User"

        button.click()
        assert page_object.get_section_heading().text == "Admin Toolbox :: All Projects : Register New User"

        page_object.fill_new_user_form(username, password, role)

        popup = page_object.check_element_presence(By.ID, "errormessage")

        assert popup.text == "That username is already taken. You will need to choose another one."

    def test_step4_logout(self, browser, baseurl):
        page_object = LoggedInPage(browser, baseurl)
        page_object.logout()
