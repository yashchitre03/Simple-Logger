from simpleLogger import Log
import pytest

"""
Test the basic working of the library and the original function.
"""

# set the configuration file path
Log.set_config_path('config.yaml')


@pytest.fixture
def setup():
    """
    Cleans the log files before each test.
    """

    return open('tests/logs/test.log', 'w').close()


@Log(profile='clean')
def dummy(x, y):
    """
    Dummy function to test the functionality of the logging decorator.
    :return: Addition of two variables.
    """

    return x + y


def test_config_path(setup):
    """
    Test if configuration path is set correctly.
    :param setup: setup: pre-run setups
    :return: None
    """

    assert Log.CONFIG_FILE is not None


@pytest.mark.parametrize("a, b, c", [(1, 2, 3), (5, 5, 10), (-50, 7, -43)])
def test_basic(setup, a, b, c):
    """
    Test if the original function runs correctly for different inputs.
    :param setup: setup: pre-run setups
    :param a: input 1
    :param b: input 2
    :param c: expected output
    :return: None
    """

    assert dummy(a, b) == c


def test_logs(setup):
    """
    Test whether basic log operations are being executed.
    :param setup: setup: pre-run setups
    :return: None
    """

    dummy(10, 20)
    with open('tests/logs/test.log') as f:
        content = f.read()
        assert '[INFO]' in content
