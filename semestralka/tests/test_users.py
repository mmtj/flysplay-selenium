import pytest
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from base import Base
from models import Page, LoginPage, LoggedInPage, ProjectPage, AdministrationPage

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

    @pytest.fixture
    def button_label(self):
        return "Register New User"

    def test_step1_login_as_admin(self, browser, baseurl):
        page_object = LoginPage(browser, baseurl)
        page_object.go_to_url()

        page_object.go_to_login_form()
        page_object.log_in("admin", "admin123")

        page_object = LoggedInPage(browser, baseurl)

        assert page_object.is_logged()

    def test_step2_has_admin_privileges(self, browser, baseurl):
        page_object = LoggedInPage(browser, baseurl)
        assert page_object.has_admin_privileges()

    def test_step3_go_to_administration(self, browser, baseurl):
        page_object = LoggedInPage(browser, baseurl)
        page_object.go_to_site_admin()

        assert page_object.get_section_heading().text == "Administrator's Toolbox :: Preferences"

    @pytest.mark.parametrize("username,password,role", testusersdata)
    def test_step4_add_new_user(
                                        self,
                                        browser,
                                        baseurl,
                                        button_label,
                                        username,
                                        password,
                                        role):
        page_object = AdministrationPage(browser, baseurl)
        page_object.users_and_groups()

        button = browser.find_element_by_link_text(button_label)
        assert button.text == button_label

        button.click()
        assert page_object.get_section_heading().text == "Admin Toolbox :: All Projects : Register New User"

        page_object.fill_new_user_form(username, password, role)
        page_object.submit_new_user_form()

        popup = browser.find_element_by_class_name("success")
        assert popup.text == "New User Account has been created."

    def test_step5_logout(self, browser, baseurl):
        page_object = LoggedInPage(browser, baseurl)
        page_object.logout()


class TestCreateUsersPairWise(Base):
    """Create new users with pairs permutations"""

    @pytest.fixture
    def button_label(self):
        return "Register New User"

    @pytest.fixture
    def button_label_view(self):
        return "View All Users"

    @pytest.mark.usesfixtures("admin_login", "admin_password")
    def test_step1_login_as_admin(self, browser, baseurl, admin_login, admin_password):
        self.login(browser, baseurl, admin_login, admin_password)

    def test_step2_has_admin_privileges(self, browser, baseurl):
        page_object = LoggedInPage(browser, baseurl)
        assert page_object.has_admin_privileges()

    def test_step3_go_to_administration(self, browser, baseurl):
        page_object = LoggedInPage(browser, baseurl)
        page_object.go_to_site_admin()

        assert page_object.get_section_heading().text == "Administrator's Toolbox :: Preferences"

    @pytest.mark.usefixtures("pairwise_data")
    def test_register_new_users(self, browser, baseurl, button_label, pairwise_data):
        username, password, role, timezone, notification = pairwise_data
        page_object = AdministrationPage(browser, baseurl)
        page_object.users_and_groups()

        button = browser.find_element_by_link_text(button_label)
        assert button.text == button_label

        button.click()
        assert page_object.get_section_heading().text == "Admin Toolbox :: All Projects : Register New User"

        page_object.fill_new_user_form(username, password, role, timezone, notification)
        page_object.submit_new_user_form()

        popup = browser.find_element_by_class_name("success")
        assert popup.text == "New User Account has been created."

    @pytest.mark.usefixtures("users_to_remove")
    def test_delete_new_users(self, browser, baseurl, button_label_view, users_to_remove):
        page_object = AdministrationPage(browser, baseurl)
        page_object.users_and_groups()

        button = browser.find_element_by_link_text(button_label_view)
        assert button.text == button_label_view

        button.click()
        assert page_object.get_section_heading().text == "Admin Toolbox :: All Projects : View All Users"

        # find checkbox that is in first td of row
        xpath_tpl = '//*[@id="editallusers"]/table//td[text() = "{}"]/../td/input'

        for username in users_to_remove:
            chkbox = browser.find_element_by_xpath(xpath_tpl.format(username))
            chkbox.click()

        browser.find_element_by_name("delete").click()

        popup = browser.find_element_by_id("successanderrors")

        assert popup.text == "Users sucessfully updated"

    def test_step5_logout(self, browser, baseurl):
        self.logout(browser, baseurl)


class TestCreateUserWhichExists(Base):
    """Test if adding new user with existing username fails"""
    @pytest.fixture
    def button_label(self):
        return "Register New User"

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
    def test_step3_dont_add_existing_user(
                                        self,
                                        browser,
                                        baseurl,
                                        button_label,
                                        username,
                                        password,
                                        role):
        page_object = AdministrationPage(browser, baseurl)
        page_object.users_and_groups()

        button = browser.find_element_by_link_text(button_label)
        assert button.text == button_label

        button.click()
        assert page_object.get_section_heading().text == "Admin Toolbox :: All Projects : Register New User"

        page_object.fill_new_user_form(username, password, role)

        popup = page_object.check_element_presence(By.ID, "errormessage")

        assert popup.text == "That username is already taken. You will need to choose another one."

    def test_step4_logout(self, browser, baseurl):
        page_object = LoggedInPage(browser, baseurl)
        page_object.logout()


class TestTryAdminPrivilegesAsNonAdmin(Base):
    """Non admin user shouldn't have admin privileges."""

    def test_step1_login_as_user(self, browser, baseurl):
        page_object = LoginPage(browser, baseurl)
        page_object.go_to_url()

        page_object.go_to_login_form()
        page_object.log_in("developer", "passw0rd")

        page_object = LoggedInPage(browser, baseurl)

        assert page_object.is_logged()

    def test_step2_user_has_not_admin_privileges(self, browser, baseurl):
        with pytest.raises(NoSuchElementException):
            page_object = LoggedInPage(browser, baseurl)
            page_object.has_admin_privileges()


class TestDeleteUsers(Base):
    """Delete users created during tests"""
    @pytest.fixture
    def button_label(self):
        return "View All Users"

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

    def test_step3_delete_users(self, browser, baseurl, button_label):
        page_object = AdministrationPage(browser, baseurl)
        page_object.users_and_groups()

        button = browser.find_element_by_link_text(button_label)
        assert button.text == button_label

        button.click()
        assert page_object.get_section_heading().text == "Admin Toolbox :: All Projects : View All Users"

        # find checkbox that is in first td of row
        xpath_tpl = '//*[@id="editallusers"]/table//td[text() = "{}"]/../td/input'

        chkbox1 = browser.find_element_by_xpath(xpath_tpl.format("developer"))
        chkbox2 = browser.find_element_by_xpath(xpath_tpl.format("reporter"))
        chkbox1.click()
        chkbox2.click()

        browser.find_element_by_name("delete").click()

        popup = browser.find_element_by_id("successanderrors")

        assert popup.text == "Users sucessfully updated"
