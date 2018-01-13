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

    def open_new_task_anonymously(self):
        self.browser.find_element_by_link_text("Open a new Task anonymously").click()

    def go_to_tasklist(self):
        self.browser.find_element_by_link_text("Tasklist").click()

    def get_popup_message(self):
        return self.browser.find_element_by_class_name("success")

    def _submit_form(self):
        """Submit buttons are usually named 'positive'"""
        self.browser.find_element_by_class_name("positive").click()


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

    def fill_new_user_form(self, username, password, role, timezone=None, notification=None):
        f_username = self.browser.find_element_by_id("username")
        f_password = self.browser.find_element_by_id("userpass")
        f_password2 = self.browser.find_element_by_id("userpass2")
        f_name = self.browser.find_element_by_id("realname")
        f_email = self.browser.find_element_by_id("emailaddress")
        f_email2 = self.browser.find_element_by_id("verifyemailaddress")
        f_role = Select(self.browser.find_element_by_id("groupin"))

        if timezone:
            f_timezone = Select(self.browser.find_element_by_id("time_zone"))
            f_timezone.select_by_visible_text(timezone)

        if notification:
            f_notification = Select(self.browser.find_element_by_id("notify_type"))
            f_notification.select_by_visible_text(notification)

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


class IssuePage(Page):
    """Issue page model"""
    def go_to_page(self):
        self.browser.find_element_by_link_text("Add new task").click()

    def go_to_issue(self, name):
        self.browser.find_element_by_link_text(name).click()

    def create_anon_issue(self, summary, desc, email):
        f_summary = self.browser.find_element_by_id("itemsummary")
        f_desc = self.browser.find_element_by_id("details")
        f_email = self.browser.find_element_by_id("anon_email")

        f_summary.send_keys(summary)
        f_desc.send_keys(desc)
        f_email.send_keys(email)

        self.browser.find_element_by_class_name("positive").click()

    def create_issue(self, summary, desc, milestone=None):
        f_summary = self.browser.find_element_by_id("itemsummary")
        f_desc = self.browser.find_element_by_id("details")

        if milestone:
            f_version = Select(self.browser.find_element_by_id("dueversion"))
            f_version.select_by_visible_text(milestone)

        f_summary.send_keys(summary)
        f_desc.send_keys(desc)

        self._submit_form()

    def find_issue(self, name):
        """Jump to issue via search box"""
        finder = self.browser.find_element_by_id("task_id")
        finder.send_keys(name + Keys.ENTER)

    def resolve_issue(self):
        self.browser.find_element_by_id("closetask").click()

        select = Select(self.browser.find_element_by_name("resolution_reason"))
        select.select_by_visible_text("Implemented")

        reason = self.browser.find_element_by_id("closure_comment")
        reason.send_keys("Closed by selenium test")

        self.browser.find_element_by_xpath('//*[@id="formclosetask"]/button').click()

    def comment_issue(self, text):
        texarea = self.browser.find_element_by_id("comment_text")
        texarea.send_keys(text)

        self._submit_form()

    def edit_issue_priority(self):
        """Change task priority to high"""
        self.browser.find_element_by_id("edittask").click()

        select = Select(self.browser.find_element_by_id("priority"))
        select.select_by_visible_text("High")

        self._submit_form()

    def get_issue_heading(self):
        return self.browser.find_element_by_xpath('//*[@id="taskdetailsfull"]/h2')

    def find_comment(self, comment):
        return self.browser.find_element_by_xpath('//div[@id="comments"]//div[@class="commenttext"]/p[1]')


class VersionPage(Page):
    """Page for versioning of project"""
    def _submit_update(self):
        update_btn = self.browser.find_element_by_xpath('//*[@id="listTable"]/tfoot/tr/td[2]/button')
        update_btn.click()

    def go_to_project_settings(self):
        self.browser.find_element_by_link_text("Manage Project").click()

    def go_to_version(self):
        self.browser.find_element_by_link_text("Versions").click()

    def create_milestone(self, milestone):
        f_version = self.browser.find_element_by_id("listnamenew")
        f_version.send_keys(milestone)

        f_tense = Select(self.browser.find_element_by_id("tensenew"))
        f_tense.select_by_visible_text("Future")

        self._submit_form()

    def remove_milestone(self, milestone):
        xpath_tpl = "//table[@id='listTable']//input[@value='{}']/../../td[5]/input"
        chkbox = self.browser.find_element_by_xpath(xpath_tpl.format(milestone))
        chkbox.click()

        self._submit_update()

    def close_milestone(self, milestone):
        """Close milestone by making it present => current version"""
        xpath_tpl = "//table[@id='listTable']//input[@value='{}']/../../td[4]/select"

        f_tense = Select(self.browser.find_element_by_xpath(xpath_tpl.format(milestone)))
        f_tense.select_by_visible_text("Present")

        self._submit_update()
