import os
import glob
import pytest


@pytest.fixture(scope="function")
def make_files(request, get_samplenum, tmpdir):
    """This fixture sets up part of the test by creating Hello World files, the
    number of files can be modified by the command line parameter for
    --samplenum defined in the conftest"""
    if get_samplenum > 10:
        request.session.logger.warning("Max samples number changed to 10.")
        get_samplenum = 10
    elif get_samplenum < 1:
        request.session.logger.warning("Min samples number changed to 1")
        get_samplenum = 1

    request.session.logger.info("Creating {} 'HELLO WORLD' files".format(get_samplenum))
    for i in range(get_samplenum):
        dest = os.path.join(tmpdir.strpath, "helloworld_{}.txt".format(i))
        with open(dest, "w") as f:
            f.write("HELLO WORLD {}".format(i))

    return get_samplenum

@pytest.mark.numbers
def test_check_num_files(request, make_files, tmpdir):
    count = len(glob.glob("{}/*.txt".format(tmpdir.strpath)))
    request.session.logger.info("Verifying that the number of hello world files is {}".format(make_files))
    assert count == make_files
