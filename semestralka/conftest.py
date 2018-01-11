import pytest


def pytest_runtest_makereport(item, call):
    if "incremental" in item.keywords:
        if call.excinfo is not None:
            parent = item.parent
            parent._previousfailed = item


def pytest_runtest_setup(item):
    if "incremental" in item.keywords:
        previousfailed = getattr(item.parent, "_previousfailed", None)
        if previousfailed is not None:
            pytest.xfail("previous test failed (%s)" %previousfailed.name)

# fixtures
@pytest.fixture()
def milestone_lifecycle():
    return "Lifecycle test milestone"


@pytest.fixture()
def milestone_lifecycle_issue_name():
    return "Test milestone issue"


@pytest.fixture()
def private_project():
    return "ZKS Private project"
