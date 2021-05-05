from simpleLogger import Log
import pytest

Log.set_config_path('config.yaml')


@pytest.fixture
def setup():
    return open('tests/logs/test.log', 'w').close()


@pytest.mark.parametrize("a, b, c", [(1, 2, 3), (5, 5, 10), (-50, 7, -43)])
def test_basic(setup, a, b, c):

    @Log(profile='clean')
    def basic_sample(x, y):
        return x + y

    assert basic_sample(a, b) == c
