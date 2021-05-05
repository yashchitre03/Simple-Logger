import time
import pytest
from simpleLogger import Log
from matplotlib import pyplot as plt

run_performance_test = False


def setup():
    return open('tests/logs/test.log', 'w').close()


def intensive_work(limit: int) -> None:
    temp = []
    for i in range(limit):
        temp.append(i)

    while temp:
        temp.pop()


@pytest.mark.skipif(run_performance_test is False, reason='Being time intensive, it is preferable to be run separately')
def test_time():
    time_original, time_with_logging, impact, difference, indices = [], [], [], [], []
    decorated_fn = Log(profile='clean')(intensive_work)

    for i in (j**2 for j in range(10, 100, 10)):
        setup()

        start = time.time()
        for times in range(100):
            intensive_work(i)
        time_original.append(time.time() - start)

        start = time.time()
        for times in range(100):
            decorated_fn(i)
        time_with_logging.append(time.time() - start)

        try:
            impact.append((time_with_logging[-1] - time_original[-1]) * 100 / time_with_logging[-1])
        except ZeroDivisionError:
            impact.append(0)

        indices.append(i)
        difference.append(time_with_logging[-1] - time_original[-1])

    plt.plot(indices, impact)
    plt.xlabel('Function complexity (loop size)')
    plt.ylabel('Time difference (%)')
    plt.title('Impact of function complexity')
    plt.savefig('tests/plots/impact_plot.png', bbox_inches='tight')
    plt.show()
