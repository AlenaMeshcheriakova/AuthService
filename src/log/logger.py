import logging
from typing import Union
from functools import wraps
import sys


class CustomLogger:

    filename: str

    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            fmt="%(asctime)s %(levelname)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def get_logger(self, name=None):
        return logging.getLogger(name)

def get_default_logger():
    return CustomLogger().get_logger()

def log_decorator(_func=None, *, my_logger: Union[CustomLogger, logging.Logger] = None):
    def decorator_log(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if my_logger is None:
                logger = get_default_logger()
            else:
                if isinstance(my_logger, CustomLogger):
                    logger = my_logger.get_logger(func.__name__)
                else:
                    logger = my_logger
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)
            logger.debug(f"function {func.__name__} called with args {signature}")
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                logger.exception(f"Exception raised in {func.__name__}. exception: {str(e)}")
                raise e
        return wrapper

    if _func is None:
        return decorator_log
    else:
        return decorator_log(_func)