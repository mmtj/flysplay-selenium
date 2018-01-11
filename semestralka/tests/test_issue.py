import pytest

from selenium.common.exceptions import NoSuchElementException

from base import Base
from models import Page
from models import AdministrationPage
from models import IssuePage


#class TestCreateIssueInPublicProject(Base):
#    def test_create_issue(self, browser, baseurl):
#        page_object = Page(browser, baseurl)
#        page_object.go_to_url()
#        page_object.open_new_task_anonymously()
#
#        issue_page_object = IssuePage(browser, baseurl)
#        issue_page_object.create_anon_issue("Test anon issue", "Testing anonymous issue submission", "anonymous@anon.ym")
#
#        popup = browser.find_element_by_class_name("success")
#        assert popup.text == "Your new task has been added."
#
#
#class TestCreateIssueInPrivateProject(Base):
#    def test_login(self, browser, baseurl):
#        self.login(browser, baseurl, "admin", "admin123")
#
#    def test_create_issue(self, browser, baseurl):
#        page_object = IssuePage(browser, baseurl)
#        page_object.switch_project("ZKS Private project")
#        page_object.go_to_page()
#        page_object.create_issue("Test issue", "Testing issue submission")
#
#        popup = browser.find_element_by_class_name("success")
#        assert popup.text == "Your new task has been added."
#
#    def test_logout(self, browser, baseurl):
#        self.logout(browser, baseurl)
#
#
#class TestFindPublicIssue(Base):
#    @pytest.mark.parametrize("issue_name", [("Test anon issue")])
#    def test_find_issue(self, browser, baseurl, issue_name):
#        page_object = IssuePage(browser, baseurl)
#        page_object.go_to_url()
#        page_object.find_issue(issue_name)
#        page_object.go_to_issue(issue_name)
#
#        heading = page_object.get_issue_heading()
#
#        assert issue_name in heading.text
#
#
#class TestFindPrivateIssue(Base):
#    def test_login(self, browser, baseurl):
#        self.login(browser, baseurl, "admin", "admin123")
#
#    @pytest.mark.parametrize("issue_name", [("Test issue")])
#    def test_find_issue(self, browser, baseurl, issue_name):
#        page_object = IssuePage(browser, baseurl)
#        page_object.switch_project("ZKS Private project")
#        page_object.go_to_issue(issue_name)
#
#        heading = page_object.get_issue_heading()
#
#        assert issue_name in heading.text
#
#    def test_logout(self, browser, baseurl):
#        self.logout(browser, baseurl)
#
#
#class TestFindPrivateIssueWithoutLogging(Base):
#    """
#    Try to access issue in private repository
#    It should FAIL
#    """
#    @pytest.mark.xfail(raises=NoSuchElementException)
#    @pytest.mark.parametrize("issue_name", [("Test issue")])
#    def test_find_issue(self, browser, baseurl, issue_name):
#        page_object = IssuePage(browser, baseurl)
#        page_object.go_to_url()
#        page_object.find_issue(issue_name)
#        page_object.go_to_issue(issue_name)


class TestIssueLifeCycle(Base):
    def test_login(self, browser, baseurl):
        self.login(browser, baseurl, "admin", "admin123")

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


# class TestCreateMilestone(Base):
#     def test_login(self):
#         pass
# 
#     def test_create_milestone(self):
#         pass
# 
#     def test_logout(self):
#         pass
# 
# 
# class TestDeleteMilestone(Base):
#     def test_login(self):
#         pass
# 
#     def test_delete_milestone(self):
#         pass
# 
#     def test_logout(self):
#         pass
# 
# 
# class TestMilestoneLifeCycle(Base):
#     """
#     Test full live cycle of milestone:
# 
#     create milestone->assign issue->resolve issue->resolve milestone
#     """
#     def test_login(self):
#         pass
# 
#     def test_create_milestone(self):
#         pass
# 
#     def test_add_issue(self):
#         pass
# 
#     def test_resolve_issue(self):
#         pass
# 
#     def test_close_milestone(self):
#         pass
# 
#     def test_logout(self):
#         pass
