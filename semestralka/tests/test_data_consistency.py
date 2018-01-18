import pytest
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select

from base import Base
from models import LoginPage, LoggedInPage, AdministrationPage


class TestUserDataConsistency(Base):
    """Create new user and check user entity consistency"""

    @pytest.fixture
    def user_metadata(self):
        return ("consistency_user", "consistency_passwd", "Basic")

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

    @pytest.mark.parametrize("button_label", [("Register New User")])
    def test_step4_add_new_user(
                                    self,
                                    browser,
                                    baseurl,
                                    button_label,
                                    user_metadata
                                ):
        page_object = AdministrationPage(browser, baseurl)
        page_object.users_and_groups()

        button = browser.find_element_by_link_text(button_label)
        assert button.text == button_label

        button.click()
        assert page_object.get_section_heading().text == "Admin Toolbox :: All Projects : {}".format(button_label)

        username, password, role = user_metadata

        page_object.fill_new_user_form(username, password, role)
        page_object.submit_new_user_form()

        popup = browser.find_element_by_class_name("success")
        assert popup.text == "New User Account has been created."

    @pytest.mark.parametrize("button_label", [("View All Users")])
    def test_step5_check_if_user_exists(
                                            self,
                                            browser,
                                            baseurl,
                                            button_label,
                                            user_metadata
                                        ):
        page_object = AdministrationPage(browser, baseurl)
        page_object.users_and_groups()

        button = browser.find_element_by_link_text(button_label)
        assert button.text == button_label

        button.click()
        assert page_object.get_section_heading().text == "Admin Toolbox :: All Projects : {}".format(button_label)

        username = user_metadata[0]
        real_name = username.upper()
        email = "{}@zks.test".format(username)
        group = user_metadata[2]

        xpath_tpl = '//*[@id="editallusers"]/table//td[text() = "{}"]/../td[2]/a'
        browser.find_element_by_xpath(xpath_tpl.format(username)).click()

        assert page_object.get_section_heading().text == "Administrator's Toolbox :: Edit user : {}".format(username)

        s_real_name = browser.find_element_by_xpath('//*[@id="toolbox"]/fieldset//li[./label/text()="Real Name"]/input').get_attribute("value")
        assert s_real_name == real_name

        s_email = browser.find_element_by_xpath('//*[@id="toolbox"]/fieldset//li[./label/text()="Email Address"]/input').get_attribute("value")
        assert s_email == email

        s_group_drop_down = Select(browser.find_element_by_xpath('//*[@id="toolbox"]/fieldset//li[./label/text()="Global Group"]/select'))
        group_exists = False

        for opt in s_group_drop_down.options:
            if opt.text == group:
                group_exists = True
                break

        assert group_exists

    def test_step6_logout(self, browser, baseurl):
        self.logout(browser, baseurl)
