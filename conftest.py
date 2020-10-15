"""
This is an example of a conftest file. Conftests are used by PyTest to setup
fixtures, command line arguments, test parameters, or to customize any part of
the Pytest test workflow.

When the pytest command is invoked it will search recursively for all conftest
files up the file system directory tree, effectively applying all fixtures and
pytest hook modifications. When there are duplicate definitions across the set
of conftest files for any given pytest fixture, the one closest to the any given
test will apply.
"""
import os
import pytest
import logging

LOGGER = logging.getLogger('pytest-sample')


# This is an example of a fixture
@pytest.fixture(scope="session")
# there are 4 scopes, [session, module, class, function] - ordered from greatest
# to smallest. This defines how often this particular fixture will be
# recaluclated with respect to each test. Session scope is only computed once.
def get_current_directory(request):
    # A fixture can be used to set up stuff for a test, print information, and
    # pass information along to the tests
    print("Current Directory Called")
    # When a fixture returns something, that value gets passed to the test
    return os.getcwd()


@pytest.fixture(scope="module")
def get_samplenum(request):
    LOGGER.info("Getting Sample Number from Args: {}".format(request.config.getoption("--samplenum")))
    return int(request.config.getoption("--samplenum"))


def pytest_addoption(parser):
    """ PyTest Hook which sets up custom Command Line Args """
    parser.addoption("--samplenum", action="store", default=1, help="Sample input number from the cmdline")



def pytest_sessionstart(session):
    """ Set up stuff for the whole session"""
    global LOGGER

    log_directory = os.path.join(os.getcwd(), "logs")
    if not os.path.exists(log_directory):
        os.mkdir(log_directory)

    ## -- Setup Logging 
    hdlr = logging.FileHandler(
        os.path.join(log_directory, "session.log")
    )

    fmttr = logging.Formatter("%(asctime)s [%(levelname)8s] --> (%(name)s): %(message)s", "%Y-%m-%d %H:%M:%S")
    hdlr.setLevel(logging.DEBUG)
    hdlr.setFormatter(fmttr)

    LOGGER.setLevel(logging.DEBUG)
    LOGGER.addHandler(hdlr)

    session.logger = LOGGER
    LOGGER.info("v"*40)
    LOGGER.info("Pytest Session Starting")


def pytest_sessionfinish(session):
    LOGGER.info("Pytest Session Completed")
    LOGGER.info("^" * 40)


def pytest_runtest_setup(item):
    LOGGER.info("Pytest Test Setup: {}".format(item.name))


def pytest_runtest_call(item):
    LOGGER.info("Pytest Test Called: {}".format(item.name))


def pytest_runtest_teardown(item):
    LOGGER.info("Pytest Test Teardown: {}".format(item.name))
