import inspect
import logging
import logging.config
import os.path
import threading
import time
from functools import wraps
import yaml
import psutil


class Log:

    CONFIG_FILE = None
    lock = threading.Lock()
    res = None

    @classmethod
    def set_config_path(cls, path):
        if os.path.isabs(path):
            cls.CONFIG_FILE = path
        else:
            frame = inspect.stack()[1]
            dirname = os.path.dirname(frame[1])
            cls.CONFIG_FILE = dirname + os.sep + path

    def __init__(self, backup_fn=None, profile=None):
        self.backup_fn = backup_fn

        try:
            with open(self.CONFIG_FILE, 'r') as f:
                log_config = yaml.load(f, Loader=yaml.FullLoader)

            logging.config.dictConfig(log_config)
            if profile in log_config['loggers']:
                self.logger = logging.getLogger(profile)
            else:
                raise KeyError('Log configuration file is incorrect or does not contain the required keys')
        except Exception as e:
            self.logger = logging.getLogger('default_root')

    def __call__(self, fn):
        self.fn = fn

        @wraps(fn)
        def wrapper(*args, **kwargs):
            return self.run(*args, **kwargs)

        return wrapper

    def run(self, *args, **kwargs):
        self.check_types(*args, **kwargs)

        execution = threading.Thread(target=self.execute, args=(*args, ), kwargs={**kwargs, })
        monitoring = threading.Thread(target=self.monitor, args=(execution, ))

        execution.start()
        monitoring.start()
        execution.join()
        monitoring.join()

        return self.res

    def check_types(self, *args, **kwargs):
        sign = inspect.signature(self.fn)
        arguments = sign.bind(*args, **kwargs).arguments
        parameters = self.fn.__annotations__

        for var in parameters.keys():
            if var in arguments and not isinstance(arguments[var], parameters[var]):
                self.logger.error(f'Type mismatch of `{var}` in `{self.fn.__name__}`: Expected {parameters[var]}; Received {type(arguments)}.')

    def execute(self, *args, **kwargs):
        with self.lock:
            self.logger.info(f'`{self.fn.__name__}` started executing')

        start = time.time()
        try:
            self.res = self.fn(*args, **kwargs)
        except Exception as e:
            with self.lock:
                self.logger.error(f'{repr(e)} occurred in `{self.fn.__name__}`. Executing the backup function instead.')
            self.res = self.backup_fn()
        else:
            end = time.time()
            with self.lock:
                self.logger.info(f'`{self.fn.__name__}` finished successfully in {round(end - start, 4)} seconds')

    def monitor(self, main_thread):
        cpu_usage, mem_usage, i = 0, 0, 1
        process = psutil.Process()
        while main_thread.is_alive():
            cpu_usage += process.cpu_percent() / psutil.cpu_count()
            mem_usage += process.memory_info().rss / 1024 ** 2
            i += 1

        with self.lock:
            self.logger.info(f'`{self.fn.__name__}` average usage: CPU = {round(cpu_usage/i, 4)}%  |   Memory = {round(mem_usage/i, 4)}MB')
