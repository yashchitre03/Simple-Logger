import time
from simpleLogger import Log


def setup():
    return open('tests/logs/test.log', 'w').close()


def intensive_work(limit: int) -> None:
    temp = []
    for i in range(limit):
        temp.append(i)

    while temp:
        temp.pop()


def test_time():
    time_original, time_with_logging, impact = [], [], []
    decorated_fn = Log(profile='clean')(intensive_work)
    arg = 100000

    for i in (j**2 for j in range(1, 35)):
        setup()

        start = time.time()
        for times in range(i):
            intensive_work(arg)
        time_original.append(time.time() - start)

        start = time.time()
        for times in range(i):
            decorated_fn(arg)
        time_with_logging.append(time.time() - start)

        try:
            impact.append((time_original[-1] - time_with_logging[-1]) * 100 / time_with_logging[-1])
        except ZeroDivisionError:
            impact.append(0)

    print(sum(impact) / len(impact))
    print(time_original[-1], time_with_logging[-1], impact[-1])
    print(impact)
    assert sum(impact) / len(impact) < 150
