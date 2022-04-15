import functools
import logging
import time

logger = logging.getLogger(__name__)


def timed(return_time=False):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            ret = func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time
            logger.info(f"runtime ({func.__name__}): {elapsed_time}s")
            if return_time:
                return ret, elapsed_time
            return ret

        return wrapper

    return decorator
