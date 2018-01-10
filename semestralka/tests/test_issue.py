import pytest

from base import Base
from models import Page, LoginPage, LoggedInPage, AdministrationPage, ProjectPage
from models import IssuePage


class TestCreateIssueInPublicProject(Base):
    def test_create_issue(self):
        pass


class TestCreateIssueInPrivateProject(Base):
    def test_login(self, browser, baseurl):
        self.login(browser, baseurl, "admin", "admin123")

    # def test_create_issue(self):
    #     pass

    def test_logout(self, browser, baseurl):
        self.logout(browser, baseurl)


# class TestFindPublicIssue(Base):
#     def test_find_issue(self):
#         pass
# 
# 
# class TestFindPrivateIssue(Base):
#     def test_login(self):
#         pass
# 
#     def test_find_issue(self):
#         pass
# 
#     def test_logout(self):
#         #self.logout()
#         pass
# 
# 
# class TestFindPrivateIssueWithoutLogging(Base):
#     def test_find_issue(self):
#         pass
# 
# 
# class TestDeleteIssueInPublicProject(Base):
#     def test_find_issue(self):
#         pass
# 
#     def test_delete_issue(self):
#         pass
# 
# 
# class TestDeleteIssueInPrivateProject(Base):
#     def test_login(self):
#         pass
# 
#     # @pytest.mark.parametrize('issueno', [(), ()])
#     # def test_delete_issue(self, issueno):
#     def test_delete_issue(self):
#         pass
# 
#     def test_logout(self):
#         pass
# 
# 
# class TestIssueLifeCycle(Base):
#     def login(self):
#         pass
# 
#     def test_create_issue(self):
#         pass
# 
#     def test_comment_issue(self):
#         pass
# 
#     def test_edit_issue(self):
#         pass
# 
#     def test_resolve_issue(self):
#         pass
# 
#     def test_logout(self):
#         pass
# 
# 
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
