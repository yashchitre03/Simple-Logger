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
    """
    This class manages all the logging responsibilities of the library.
    This class will also be used by the user to decorate their function with logging capabilities.
    """

    CONFIG_FILE = None  # path to the configuration file to be set by the user.
    lock = threading.Lock()  # lock to avoid race conditions to the log files.
    res = None  # the result after running either the main function or the backup function provided by the user.

    @classmethod
    def set_config_path(cls, path: str) -> None:
        """
        Allows the user to provide a configuration file for logging instead of using the default logging.
        :param path: path to the configuration file (either relative or absolute path).
        :return: None
        """

        if os.path.isabs(path):  # checks if the path is absolute
            cls.CONFIG_FILE = path
        else:  # converts relative path to absolute path
            frame = inspect.stack()[1]
            dirname = os.path.dirname(frame[1])  # get the directory of the caller.
            cls.CONFIG_FILE = dirname + os.sep + path

    def __init__(self, backup_fn=None, profile=None):
        """
        Constructor is called with all the arguments passed to the logging library.
        :param backup_fn: The function to execute if the main function fails (could be an anonymous function).
        :param profile: User can create many different logging styles in the configuration file,
         and provide its id as the profile.
        """

        self.backup_fn = backup_fn  # save the backup function

        try:  # if any issues are encountered in accessing the config file or the profile is not present,
            # default configuration is used instead.
            with open(self.CONFIG_FILE, 'r') as f:
                log_config = yaml.load(f, Loader=yaml.FullLoader)

            logging.config.dictConfig(log_config)
            if profile in log_config['loggers']:
                self.logger = logging.getLogger(profile)
            else:
                raise KeyError('Log configuration file is incorrect or does not contain the required keys')
        except (OSError, IOError, KeyError):  # use default config
            self.logger = logging.getLogger('default_root')

    def __call__(self, fn):
        """
        This method is invoked to create a wrapper.
        A wrapper is returned that has access to the original function.
        :param fn: The original function which was decorated.
        :return wrapper: A wrapper object of a decorator design pattern.
        """

        self.fn = fn  # save the original function

        @wraps(fn)  # this annotation makes sure all the attributes
        # and documentation of the original function is not overridden.
        def wrapper(*args, **kwargs):
            return self.run(*args, **kwargs)

        return wrapper

    def run(self, *args, **kwargs):
        """
        Whenever the original function is called, this function is called instead.
        :param args: Any positional arguments of the original function.
        :param kwargs: Any key-worded arguments of the original function.
        :return: result/return value after executing the function.
        """

        self.check_types(*args, **kwargs)  # check for type conflicts

        # thread for function execution
        execution = threading.Thread(target=self.execute, args=(*args,), kwargs={**kwargs, })

        # thread for function's resource monitoring
        monitoring = threading.Thread(target=self.monitor, args=(execution,))

        # starts the threads
        execution.start()
        monitoring.start()

        # Waits for both the threads to end successfully
        execution.join()
        monitoring.join()

        # returns the results
        return self.res

    def check_types(self, *args, **kwargs):
        """
        Checks and logs any type conflicts in the function
        :param args: Any positional arguments of the original function.
        :param kwargs: Any key-worded arguments of the original function.
        :return: None
        """

        # gets the function signature and parameters
        sign = inspect.signature(self.fn)
        arguments = sign.bind(*args, **kwargs).arguments
        parameters = self.fn.__annotations__

        # Matches each parameter
        for var in parameters.keys():
            if var in arguments and not isinstance(arguments[var], parameters[var]):
                self.logger.warning(f'Type conflict of `{var}` in `{self.fn.__name__}`:'
                                    f' Expected {parameters[var]}; Received {type(arguments[var])}.')

    def execute(self, *args, **kwargs):
        """
        Executes the original function and logs any issues.
        :param args: Any positional arguments of the original function.
        :param kwargs: Any key-worded arguments of the original function.
        :return: None
        """

        # thread locks are acquired each time logging is to be performed.
        with self.lock:
            # log start of execution
            self.logger.info(f'`{self.fn.__name__}` started executing')

        start = time.time()  # time the function

        try:
            self.res = self.fn(*args, **kwargs)
        except Exception as e:
            # fallback to the backup function if any exception occurs.
            with self.lock:
                self.logger.error(f'{repr(e)} occurred in `{self.fn.__name__}`. '
                                  f'Executing the backup function if provided.')
            if self.backup_fn:
                self.res = self.backup_fn()
        else:
            end = time.time()
            with self.lock:
                self.logger.info(f'`{self.fn.__name__}` finished successfully in {round(end - start, 4)} seconds')

    def monitor(self, main_thread):
        """
        Monitors the resource usage of the main function being executed.
        :param main_thread: The thread of the main function.
        :return: None
        """

        cpu_usage, mem_usage, i = 0, 0, 1  # reset the resource usage
        process = psutil.Process()  # get the current process of the threads

        while main_thread.is_alive():  # monitor as long as the main function is executing
            cpu_usage += process.cpu_percent()
            mem_usage += process.memory_info().rss
            i += 1

        # get average statistics and log them
        cpu_usage /= (psutil.cpu_count() * i)
        mem_usage /= (1024 ** 2 * i)
        with self.lock:
            self.logger.info(f'`{self.fn.__name__}` average usage: CPU = {round(cpu_usage, 4)}%'
                             f'  |   Memory = {round(mem_usage, 4)}MB')
