import logging
import time
import tracemalloc

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('[%(levelname)s] %(asctime)s : %(message)s')

file_handler = logging.FileHandler('test.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


class Helper:

    def __init__(self, fn, backup_fn=None, file='default.log'):
        self.fn = fn
        self.backup_fn = backup_fn
        self.file = file

    def __call__(self, *args, **kwargs):
        logger.info(f'`{self.fn.__name__}` started executing')
        tracemalloc.start()
        start = time.time()

        try:
            res = self.fn(*args, **kwargs)
        except Exception as e:
            logger.error(f'{repr(e)} occurred in `{self.fn.__name__}`. Executing the backup function instead.')
            res = self.backup_fn()
        else:
            end = time.time()
            logger.info(f'`{self.fn.__name__}` finished in {round(end - start, 4)} seconds with peak memory usage {tracemalloc.get_traced_memory()[1] / 10 ** 6} MB')
        finally:
            tracemalloc.stop()

        return res


def log(*args, **kwargs):
    def wrapper(fn):
        return Helper(fn, *args, **kwargs)

    return wrapper
