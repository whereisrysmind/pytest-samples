import pytest


@pytest.mark.broken
def test_failing1():
    assert False, "This test will fail"


@pytest.mark.broken
def test_failing2():
    raise Exception("This test will also fail")


@pytest.mark.xfail(reason="Its set up to fail")
def test_xfail():
    raise Exception("This Test WOULD Fail")


@pytest.mark.skip
def test_skipped():
    # This test will be skipped
    pass

#                   condition
@pytest.mark.skipif(   True  , reason="Skipped for Blah")
def test_skip_if():
    pass

@pytest.fixture
def fixture_with_error():
    raise Exception("This fixture has hit some error")


@pytest.mark.broken
def test_will_error(fixture_with_error):
    pass # this test WOULD otherwise pass.
