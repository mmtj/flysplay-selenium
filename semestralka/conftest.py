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
@pytest.fixture
def milestone_lifecycle():
    return "Lifecycle test milestone"


@pytest.fixture
def milestone_lifecycle_issue_name():
    return "Test milestone issue"


@pytest.fixture
def private_project():
    return "ZKS Private project"


@pytest.fixture
def public_project():
    return "ZKS public project"


@pytest.fixture
def future_milestone():
    return "Future test milestone"


@pytest.fixture
def admin_login():
    return "admin"


@pytest.fixture
def admin_password():
    return "admin123"

pairs_params = [
    ("user1","passw0rd","Basic","GMT","None"),
    ("user2","passw0rd","Admin","GMT","Email"),
    ("user3","passw0rd","Developers","GMT","Jabber"),
    ("user4","passw0rd","Reporters","GMT","Both"),
    ("user5","passw0rd","Basic","GMT-12","Email"),
    ("user6","passw0rd","Admin","GMT-12","None"),
    ("user7","passw0rd","Developers","GMT-12","Both"),
    ("user8","passw0rd","Reporters","GMT-12","Jabber"),
    ("user9","passw0rd","Basic","GMT-11","Jabber"),
    ("user10","passw0rd","Admin","GMT-11","Both"),
    ("user11","passw0rd","Developers","GMT-11","None"),
    ("user12","passw0rd","Reporters","GMT-11","Email"),
    ("user13","passw0rd","Basic","GMT-10","Both"),
    ("user14","passw0rd","Admin","GMT-10","Jabber"),
    ("user15","passw0rd","Developers","GMT-10","Email"),
    ("user16","passw0rd","Reporters","GMT-10","None"),
    ("user17","passw0rd","Pending","GMT-9","None"),
    ("user18","passw0rd","Basic","GMT-9","Email"),
    ("user19","passw0rd","Admin","GMT-9","Jabber"),
    ("user20","passw0rd","Developers","GMT-9","Both"),
    ("user21","passw0rd","Pending","GMT-8","Email"),
    ("user22","passw0rd","Basic","GMT-8","None"),
    ("user23","passw0rd","Admin","GMT-8","Both"),
    ("user24","passw0rd","Developers","GMT-8","Jabber"),
    ("user25","passw0rd","Pending","GMT-7","Jabber"),
    ("user26","passw0rd","Basic","GMT-7","Both"),
    ("user27","passw0rd","Admin","GMT-7","None"),
    ("user28","passw0rd","Developers","GMT-7","Email"),
    ("user29","passw0rd","Pending","GMT-6","Both"),
    ("user30","passw0rd","Basic","GMT-6","Jabber"),
    ("user31","passw0rd","Admin","GMT-6","Email"),
    ("user32","passw0rd","Developers","GMT-6","None"),
    ("user33","passw0rd","Reporters","GMT-5","None"),
    ("user34","passw0rd","Pending","GMT-5","Email"),
    ("user35","passw0rd","Basic","GMT-5","Jabber"),
    ("user36","passw0rd","Admin","GMT-5","Both"),
    ("user37","passw0rd","Reporters","GMT-4","Email"),
    ("user38","passw0rd","Pending","GMT-4","None"),
    ("user39","passw0rd","Basic","GMT-4","Both"),
    ("user40","passw0rd","Admin","GMT-4","Jabber"),
    ("user41","passw0rd","Reporters","GMT-3","Jabber"),
    ("user42","passw0rd","Pending","GMT-3","Both"),
    ("user43","passw0rd","Basic","GMT-3","None"),
    ("user44","passw0rd","Admin","GMT-3","Email"),
    ("user45","passw0rd","Reporters","GMT-2","Both"),
    ("user46","passw0rd","Pending","GMT-2","Jabber"),
    ("user47","passw0rd","Basic","GMT-2","Email"),
    ("user48","passw0rd","Admin","GMT-2","None"),
    ("user49","passw0rd","Developers","GMT-1","None"),
    ("user50","passw0rd","Reporters","GMT-1","Email"),
    ("user51","passw0rd","Pending","GMT-1","Jabber"),
    ("user52","passw0rd","Basic","GMT-1","Both"),
    ("user53","passw0rd","Developers","GMT+1","Email"),
    ("user54","passw0rd","Reporters","GMT+1","None"),
    ("user55","passw0rd","Pending","GMT+1","Both"),
    ("user56","passw0rd","Basic","GMT+1","Jabber"),
    ("user57","passw0rd","Developers","GMT+2","Jabber"),
    ("user58","passw0rd","Reporters","GMT+2","Both"),
    ("user59","passw0rd","Pending","GMT+2","None"),
    ("user60","passw0rd","Basic","GMT+2","Email"),
    ("user61","passw0rd","Developers","GMT+3","Both"),
    ("user62","passw0rd","Reporters","GMT+3","Jabber"),
    ("user63","passw0rd","Pending","GMT+3","Email"),
    ("user64","passw0rd","Basic","GMT+3","None"),
    ("user65","passw0rd","Admin","GMT+4","None"),
    ("user66","passw0rd","Developers","GMT+4","Email"),
    ("user67","passw0rd","Reporters","GMT+4","Jabber"),
    ("user68","passw0rd","Pending","GMT+4","Both"),
    ("user69","passw0rd","Admin","GMT+5","Email"),
    ("user70","passw0rd","Developers","GMT+5","None"),
    ("user71","passw0rd","Reporters","GMT+5","Both"),
    ("user72","passw0rd","Pending","GMT+5","Jabber"),
    ("user73","passw0rd","Admin","GMT+6","Jabber"),
    ("user74","passw0rd","Developers","GMT+6","Both"),
    ("user75","passw0rd","Reporters","GMT+6","None"),
    ("user76","passw0rd","Pending","GMT+6","Email"),
    ("user77","passw0rd","Admin","GMT+7","Both"),
    ("user78","passw0rd","Developers","GMT+7","Jabber"),
    ("user79","passw0rd","Reporters","GMT+7","Email"),
    ("user80","passw0rd","Pending","GMT+7","None"),
    ("user81","passw0rd","Basic","GMT+8","None"),
    ("user82","passw0rd","Admin","GMT+8","Email"),
    ("user83","passw0rd","Developers","GMT+8","Jabber"),
    ("user84","passw0rd","Reporters","GMT+8","Both"),
    ("user85","passw0rd","Basic","GMT+9","Email"),
    ("user86","passw0rd","Admin","GMT+9","None"),
    ("user87","passw0rd","Developers","GMT+9","Both"),
    ("user88","passw0rd","Reporters","GMT+9","Jabber"),
    ("user89","passw0rd","Basic","GMT+10","Jabber"),
    ("user90","passw0rd","Admin","GMT+10","Both"),
    ("user91","passw0rd","Developers","GMT+10","None"),
    ("user92","passw0rd","Reporters","GMT+10","Email"),
    ("user93","passw0rd","Basic","GMT+11","Both"),
    ("user94","passw0rd","Admin","GMT+11","Jabber"),
    ("user95","passw0rd","Developers","GMT+11","Email"),
    ("user96","passw0rd","Reporters","GMT+11","None"),
    ("user97","passw0rd","Pending","GMT+12","None"),
    ("user98","passw0rd","Basic","GMT+12","Email"),
    ("user99","passw0rd","Admin","GMT+12","Jabber"),
    ("user100","passw0rd","Developers","GMT+12","Both"),
    ("user101","passw0rd","Pending","GMT+13","Email"),
    ("user102","passw0rd","Basic","GMT+13","None"),
    ("user103","passw0rd","Admin","GMT+13","Both"),
    ("user104","passw0rd","Developers","GMT+13","Jabber"),
            ]

@pytest.fixture(params=pairs_params)
def pairwise_data(request):
    return request.param
