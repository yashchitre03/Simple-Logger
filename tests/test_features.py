from simpleLogger import Log
import pytest

"""
This file tests all the main features of the library. Some of them are:
1. Flow of control logging
2. Resource usage logging
3. Exception handling
4. Type-checking
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


def test_control_logs(setup):
    """
    Tests if flow of control is logged in the log files.
    :param setup: pre-run setups
    :return: None
    """

    dummy(10, 20)
    with open('tests/logs/test.log') as f:
        content = f.read()
        assert 'started' in content and 'finished' in content


def test_resource_logs(setup):
    """
    Tests if resource monitoring is logged in the log files.
    :param setup: pre-run setups
    :return: None
    """

    dummy(10, 20)
    with open('tests/logs/test.log') as f:
        content = f.read()
        assert 'CPU' in content and 'Memory' in content


def test_exception_logs(setup):
    """
    Tests if function exceptions is logged in the log files.
    :param setup: pre-run setups
    :return: None
    """

    dummy(10, None)
    with open('tests/logs/test.log') as f:
        content = f.read()
        assert 'backup' in content


def test_exception_handling(setup):
    """
    Tests if backup functions are executed on occurrence of exceptions.
    :param setup: pre-run setups
    :return: None
    """

    @Log(backup_fn=lambda: -1, profile='clean')
    def dummy_with_backup(x, y):
        return x + y

    assert dummy_with_backup(10, None) == -1


def test_type_logs(setup):
    """
    Tests if type-conflict is logged in the log files.
    :param setup: pre-run setups
    :return: None
    """

    @Log(profile='clean')
    def dummy_with_types(x: int, y: int) -> int:
        return x + y

    dummy_with_types('one', 'two')
    with open('tests/logs/test.log') as f:
        content = f.read()
        assert 'conflict' in content
