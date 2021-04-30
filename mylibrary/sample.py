class Logger:

    def __init__(self, fn, enter_msg='Nope', exit_msg='Nope2'):
        self.fn = fn
        self.enter_msg = enter_msg
        self.exit_msg = exit_msg

    def __call__(self, *args, **kwargs):
        print(self.enter_msg)
        res = self.fn(*args, **kwargs)
        print(self.exit_msg)
        return res


def log(*args, **kwargs):
    def wrapper(fn):
        return Logger(fn, *args, **kwargs)
    return wrapper
