import time
import pytest
from simpleLogger import Log
from matplotlib import pyplot as plt

"""
Plots the performance of the library for documentation purposes. 
Set 'run_performance_test' to True if this test is to be run.
"""

run_performance_test = False
Log.set_config_path('config.yaml')


def setup():
    """
    Cleans the log files before each test.
    """

    return open('tests/logs/test.log', 'w').close()


def intensive_work(limit: int) -> None:
    """
    A dummy function that adds a number to a list n times, and empties the list one by one.
    It is meant to simulate some kind of time-intensive work, could be replaced with any complex algorithm.
    :param limit: Length of for loop
    :return: None
    """
    temp = []
    for i in range(limit):
        temp.append(i)

    while temp:
        temp.pop()


@pytest.mark.skipif(run_performance_test is False, reason='Being time intensive, it is preferable to be run separately')
def test_time():
    """
    Plots the impact of the library on our algorithm. Set 'run_performance_test' to True to run this test.
    :return: None
    """
    time_original, time_with_logging, impact, difference, indices = [], [], [], [], []

    # manually decorate the function
    decorated_fn = Log(profile='clean')(intensive_work)

    # call the function multiple times, once without the decorator, once with it.
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

    # plot the results
    plt.plot(indices, impact)
    plt.xlabel('Function complexity (loop size)')
    plt.ylabel('Time difference (%)')
    plt.title('Impact of function complexity')
    plt.savefig('tests/plots/impact_plot.png', bbox_inches='tight')
    plt.show()
