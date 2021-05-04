import inspect
import logging
import logging.config
import os.path
from functools import wraps
import yaml


class Log:

    CONFIG_FILE = None

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
            return self.exec(*args, **kwargs)

        return wrapper

    def exec(self, *args, **kwargs):
        pass
