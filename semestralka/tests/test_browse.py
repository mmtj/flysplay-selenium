import pytest

from base import Base
from models import Page, LoginPage, LoggedInPage, AdministrationPage, ProjectPage


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
