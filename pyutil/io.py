import functools
import os
import sys


def redirect_stdout(path: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                if os.path.dirname(path):
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                ref = sys.stdout
                sys.stdout = open(path, "w")
                return func(*args, **kwargs)
            finally:
                sys.stdout = ref

        return wrapper

    return decorator
