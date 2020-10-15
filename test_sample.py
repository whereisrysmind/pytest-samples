import os
import pytest

from datetime import datetime, timedelta



def idfn(val):
    if isinstance(val, (datetime,)):
        # note this wouldn't show any hours/minutes/seconds
        return val.strftime('%Y%m%d')


@pytest.fixture(scope="class", params=range(4))
def input_numbers(request):
    request.session.logger.info("PyTest Fixture to get input numbers: {}".format(request.param))
    return request.param


# This is a simple example of parametrizing a test directly
@pytest.mark.parametrize("result", [True]) # , False])
def test_simple(result):
    # this is a test, one will pass and one will fail
    assert result


def test_get_fixture_from_conftest(get_current_directory):
    # get_current_directory is a fixture defined in tests/examples/conftest.py
    # As a session scoped fixture, it will have been computed only once, at the
    # start of the session. its task was the return the current working
    # directory.

    assert os.getcwd() == get_current_directory


timetestdata = [
    (datetime(2020, 12, 12), datetime(2020, 12, 11), timedelta(1)),
    (datetime(2020, 12, 11), datetime(2020, 12, 12), timedelta(-1)),
]

class TestGroupedInAClass:

    @pytest.mark.time
    @pytest.mark.parametrize("a,b,expected", timetestdata)
    def test_timedistance_v0(self, a, b, expected):
        diff = a - b
        assert diff == expected

    @pytest.mark.time
    @pytest.mark.parametrize("a,b,expected", timetestdata, ids=["forward", "backward"])
    def test_timedistance_v1(self, a, b, expected):
        diff = a - b
        assert diff == expected

    @pytest.mark.time
    @pytest.mark.parametrize("a,b,expected", timetestdata, ids=idfn)
    def test_timedistance_v2(self, a, b, expected):
        diff = a - b
        assert diff == expected

    @pytest.mark.numbers
    def test_even_numbers(self, input_numbers):
        if (input_numbers % 2) == 1:
            pytest.xfail("{} is ODD".format(input_numbers))

        assert (input_numbers % 2) == 0


