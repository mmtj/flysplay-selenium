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

    def go_to_site_admin(self):
        self.browser.find_element_by_class_name("fa-gears").click()

    def has_admin_privileges(self):
        return self.browser.find_element_by_class_name("fa-gears")

    def get_section_heading(self):
        return self.browser.find_element_by_tag_name("h3")


class AdministrationPage(Page):
    """Administration of Flyspray"""
    def users_and_groups(self):
        self.browser.find_element_by_id("globuglink").click()

    def register_new_user(self):
        self.browser.find_element_by_link_text("Register New User").click()

    def get_section_heading(self):
        return self.browser.find_element_by_tag_name("h3")

    def fill_new_user_form(self, username, password, role):
        f_username = self.browser.find_element_by_id("username")
        f_password = self.browser.find_element_by_id("userpass")
        f_password2 = self.browser.find_element_by_id("userpass2")
        f_name = self.browser.find_element_by_id("realname")
        f_email = self.browser.find_element_by_id("emailaddress")
        f_email2 = self.browser.find_element_by_id("verifyemailaddress")
        f_role = Select(self.browser.find_element_by_id("groupin"))

        emailaddr = "{}@zks.test".format(username)

        f_username.send_keys(username)
        f_password.send_keys(password)
        f_password2.send_keys(password)
        f_name.send_keys(username.upper())
        f_email.send_keys(emailaddr)
        f_email2.send_keys(emailaddr)
        f_role.select_by_visible_text(role)

    def submit_new_user_form(self):
        self.browser.find_element_by_id("buSubmit").click()


class ProjectPage(LoggedInPage):
    """Projects page model"""
    def go_to_project_overview_page(self):
        self.browser.find_element_by_link_text("Overview").click()

    def get_project_overview_name(self):
        h2 = self.browser.find_element_by_tag_name("h2")
        a = h2.find_element_by_tag_name("a")

        return a.text
