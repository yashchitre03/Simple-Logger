from simpleLogger import Log
import pytest

Log.set_config_path('config.yaml')


@pytest.fixture
def setup():
    return open('tests/logs/test.log', 'w').close()


@Log(profile='clean')
def dummy(x, y):
    return x + y


def test_config_path(setup):
    assert Log.CONFIG_FILE is not None


@pytest.mark.parametrize("a, b, c", [(1, 2, 3), (5, 5, 10), (-50, 7, -43)])
def test_basic(setup, a, b, c):
    assert dummy(a, b) == c


def test_logs(setup):
    dummy(10, 20)
    with open('tests/logs/test.log') as f:
        content = f.read()
        assert '[INFO]' in content
