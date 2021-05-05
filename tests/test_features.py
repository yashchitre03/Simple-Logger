from simpleLogger import Log
import pytest

Log.set_config_path('config.yaml')


@pytest.fixture
def setup():
    return open('tests/logs/test.log', 'w').close()


@Log(profile='clean')
def dummy(x, y):
    return x + y


def test_control_logs(setup):
    dummy(10, 20)
    with open('tests/logs/test.log') as f:
        content = f.read()
        assert 'started' in content and 'finished' in content


def test_resource_logs(setup):
    dummy(10, 20)
    with open('tests/logs/test.log') as f:
        content = f.read()
        assert 'CPU' in content and 'Memory' in content


def test_exception_logs(setup):
    dummy(10, None)
    with open('tests/logs/test.log') as f:
        content = f.read()
        assert 'backup' in content


def test_exception_handling(setup):

    @Log(backup_fn=lambda: -1, profile='clean')
    def dummy_with_backup(x, y):
        return x + y

    assert dummy_with_backup(10, None) == -1


def test_type_logs(setup):

    @Log(profile='clean')
    def dummy_with_types(x: int, y: int) -> int:
        return x + y

    dummy_with_types('one', 'two')
    with open('tests/logs/test.log') as f:
        content = f.read()
        assert 'conflict' in content
