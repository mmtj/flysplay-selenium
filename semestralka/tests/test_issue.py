import pytest

from selenium.common.exceptions import NoSuchElementException

from base import Base
from models import Page
from models import AdministrationPage
from models import IssuePage
from models import VersionPage

from config import admin_login, admin_password


class TestCreateIssueInPublicProject(Base):
    def test_create_issue(self, browser, baseurl):
        page_object = Page(browser, baseurl)
        page_object.go_to_url()
        page_object.open_new_task_anonymously()

        issue_page_object = IssuePage(browser, baseurl)
        issue_page_object.create_anon_issue("Test anon issue", "Testing anonymous issue submission", "anonymous@anon.ym")

        popup = browser.find_element_by_class_name("success")
        assert popup.text == "Your new task has been added."


class TestCreateIssueInPrivateProject(Base):
    def test_login(self, browser, baseurl):
        self.login(browser, baseurl, admin_login, admin_password)

    def test_create_issue(self, browser, baseurl):
        page_object = IssuePage(browser, baseurl)
        page_object.switch_project("ZKS Private project")
        page_object.go_to_page()
        page_object.create_issue("Test issue", "Testing issue submission")

        popup = browser.find_element_by_class_name("success")
        assert popup.text == "Your new task has been added."

    def test_logout(self, browser, baseurl):
        self.logout(browser, baseurl)


class TestFindPublicIssue(Base):
    @pytest.mark.parametrize("issue_name", [("Test anon issue")])
    def test_find_issue(self, browser, baseurl, issue_name):
        page_object = IssuePage(browser, baseurl)
        page_object.go_to_url()
        page_object.find_issue(issue_name)
        page_object.go_to_issue(issue_name)

        heading = page_object.get_issue_heading()

        assert issue_name in heading.text


class TestFindPrivateIssue(Base):
    def test_login(self, browser, baseurl):
        self.login(browser, baseurl, admin_login, admin_password)

    @pytest.mark.parametrize("issue_name", [("Test issue")])
    def test_find_issue(self, browser, baseurl, issue_name):
        page_object = IssuePage(browser, baseurl)
        page_object.switch_project("ZKS Private project")
        page_object.go_to_issue(issue_name)

        heading = page_object.get_issue_heading()

        assert issue_name in heading.text

    def test_logout(self, browser, baseurl):
        self.logout(browser, baseurl)


class TestFindPrivateIssueWithoutLogging(Base):
    """
    Try to access issue in private repository
    It should FAIL
    """
    @pytest.mark.xfail(raises=NoSuchElementException)
    @pytest.mark.parametrize("issue_name", [("Test issue")])
    def test_find_issue(self, browser, baseurl, issue_name):
        page_object = IssuePage(browser, baseurl)
        page_object.go_to_url()
        page_object.find_issue(issue_name)
        page_object.go_to_issue(issue_name)


class TestIssueLifeCycle(Base):
    def test_login(self, browser, baseurl):
        self.login(browser, baseurl, admin_login, admin_password)

    def test_create_issue(self, browser, baseurl):
        page_object = IssuePage(browser, baseurl)
        page_object.switch_project("ZKS Private project")
        page_object.go_to_page()
        page_object.create_issue("Test issue lifecycle", "Testing issue submission")

        popup = page_object.get_popup_message()
        assert popup.text == "Your new task has been added."

    @pytest.mark.parametrize("comment", [("Comment from selenium bot!")])
    def test_comment_issue(self, browser, baseurl, comment):
        page_object = IssuePage(browser, baseurl)
        page_object.comment_issue(comment)

        popup = page_object.get_popup_message()
        assert popup.text == "Comment has been added."

        saved_comment = page_object.find_comment(comment)
        assert saved_comment.text == comment

    def test_edit_issue_priority(self, browser, baseurl):
        page_object = IssuePage(browser, baseurl)
        page_object.edit_issue_priority()

        priority = browser.find_element_by_xpath('//*[@id="taskfields"]/ul/li[8]/span[2]')

        assert priority.text == "High"

    @pytest.mark.parametrize("issue_name", [("Test issue lifecycle")])
    def test_resolve_issue(self, browser, baseurl, issue_name):
        page_object = IssuePage(browser, baseurl)
        page_object.go_to_tasklist()
        page_object.go_to_issue(issue_name)
        page_object.resolve_issue()

        popup = page_object.get_popup_message()
        assert popup.text == "Task has been closed."

    def test_logout(self, browser, baseurl):
        self.logout(browser, baseurl)


class TestCreateMilestone(Base):
    @pytest.fixture
    def milestone(self):
        return "Future test milestone"

    @pytest.fixture
    def project(self):
        return "ZKS Private project"

    def test_login(self, browser, baseurl):
        self.login(browser, baseurl, admin_login, admin_password)

    def test_create_milestone(self, browser, baseurl, milestone, project):
        page_object = VersionPage(browser, baseurl)
        page_object.switch_project(project)
        page_object.go_to_project_settings()
        page_object.go_to_version()
        page_object.create_milestone(milestone)

        popup = page_object.get_popup_message()
        assert popup.text == "New list item added."

        xpath_tpl = "//table[@id='listTable']//input[@value='{}']"

        milestone_saved = browser.find_element_by_xpath(xpath_tpl.format(milestone))
        assert milestone_saved.get_attribute('value') == milestone

    def test_logout(self, browser, baseurl):
        self.logout(browser, baseurl)


class TestDeleteMilestone(Base):
    @pytest.fixture
    def milestone(self):
        return "Future test milestone"

    @pytest.fixture
    def project(self):
        return "ZKS Private project"

    def test_login(self, browser, baseurl):
        self.login(browser, baseurl, admin_login, admin_password)

    def test_delete_milestone(self, browser, baseurl, milestone, project):
        page_object = VersionPage(browser, baseurl)
        page_object.switch_project(project)
        page_object.go_to_project_settings()
        page_object.go_to_version()
        page_object.remove_milestone(milestone)

        with pytest.raises(NoSuchElementException):
            xpath_tpl = "//table[@id='listTable']//input[@value='{}']"
            browser.find_element_by_xpath(xpath_tpl.format(milestone))

    def test_logout(self, browser, baseurl):
        self.logout(browser, baseurl)


@pytest.mark.usefixtures(
                    "private_project",
                    "milestone_lifecycle",
                    "milestone_lifecycle_issue_name"
                        )
class TestMilestoneLifeCycle(Base):
    """
    Test full live cycle of milestone:

    create milestone->assign issue->resolve issue->resolve milestone
    """
    def test_login(self, browser, baseurl):
        self.login(browser, baseurl, admin_login, admin_password)

    def test_create_milestone(self, browser, baseurl, milestone_lifecycle, private_project):
        milestone = milestone_lifecycle
        project = private_project

        page_object = VersionPage(browser, baseurl)
        page_object.switch_project(project)
        page_object.go_to_project_settings()
        page_object.go_to_version()
        page_object.create_milestone(milestone)

        popup = page_object.get_popup_message()
        assert popup.text == "New list item added."

        xpath_tpl = "//table[@id='listTable']//input[@value='{}']"

        milestone_saved = browser.find_element_by_xpath(xpath_tpl.format(milestone))
        assert milestone_saved.get_attribute('value') == milestone

    def test_add_issue(self, browser, baseurl, milestone_lifecycle, milestone_lifecycle_issue_name, private_project):
        milestone = milestone_lifecycle
        project = private_project
        issue_name = milestone_lifecycle_issue_name

        page_object = IssuePage(browser, baseurl)
        page_object.switch_project(project)
        page_object.go_to_page()
        page_object.create_issue(issue_name, "Testing issue submission form milestone test", milestone)

        popup = page_object.get_popup_message()
        assert popup.text == "Your new task has been added."

    def test_resolve_issue(self, browser, baseurl, milestone_lifecycle_issue_name):
        issue_name = milestone_lifecycle_issue_name

        page_object = IssuePage(browser, baseurl)
        page_object.go_to_tasklist()
        page_object.go_to_issue(issue_name)
        page_object.resolve_issue()

        popup = page_object.get_popup_message()
        assert popup.text == "Task has been closed."

    def test_close_milestone(self, browser, baseurl, milestone_lifecycle, private_project):
        project = private_project
        milestone = milestone_lifecycle

        page_object = VersionPage(browser, baseurl)
        page_object.switch_project(project)
        page_object.go_to_project_settings()
        page_object.go_to_version()
        page_object.close_milestone(milestone)

        popup = page_object.get_popup_message()

        assert popup.text == "List has been updated."

    def test_logout(self, browser, baseurl):
        self.logout(browser, baseurl)
