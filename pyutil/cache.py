import functools
import logging
import os

import pandas as pd

from pyutil.dicts import sort_dict
from pyutil.hashing import hash_item
from pyutil.misc import get_full_kwargs, get_named_args

logger = logging.getLogger(__name__)


class Cache:
    def __init__(self, path: str, name: str, args: tuple, log_level: str = "INFO"):
        """Creates a cache on disk at the specified `path`. This class acts as
        a wrapper for general request functions to save the result of a request
        to disk for fast lookup later on.

        Args:
            path: Path to store cache on disk
            name: Name of function or operation being cached
            args: Arguments passed to cached function or operation for logging purposes
            log_level: level to emit logs at. defaults to INFO
        """
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        self.path = path
        self.name = name
        self.args = f"({', '.join(str(arg) for arg in args)})"
        assert log_level in logging._nameToLevel.keys()
        self.log_level = log_level

    def log(self, *msg):
        logger.log(logging._nameToLevel[self.log_level], *msg)

    def query(
        self,
        key,
        query_fn=None,
        save_fn=pd.to_pickle,
        load_fn=pd.read_pickle,
        query_fn_args=[],
        save_fn_args=[],
        load_fn_args=[],
        query_fn_kwargs={},
        save_fn_kwargs={},
        load_fn_kwargs={},
        refresh=False,
        disabled=False,
    ):
        if disabled:
            return query_fn(*query_fn_args, **query_fn_kwargs)

        if not refresh and self.search(key) is True:
            self.log(f"Using cached value in call to {self.name}{self.args} | key={key} ({self.path})")
            return load_fn(os.path.join(self.path, key), *load_fn_args, **load_fn_kwargs)
        else:
            data = query_fn(*query_fn_args, **query_fn_kwargs)
            self.log(f"Saving cached value in call to {self.name}{self.args} | key={key} ({self.path})")
            save_fn(data, os.path.join(self.path, key), *save_fn_args, **save_fn_kwargs)
            return data

    def search(self, key):
        return True if key in os.listdir(self.path) else False


def cached(
    path: str = "/tmp/cache",
    disabled: bool = False,
    refresh: bool = False,
    log_level: str = "INFO",
    identifiers: list = [],
    path_seperators: list = [],
    is_method: bool = False,
    instance_identifiers: list = [],
    instance_path_seperators: list = [],
):
    """Save the result of the decorated function in a cache. Function arguments are hashed such that subsequent
    calls with the same arguments result in a cache hit

    Args:
        path: disk path to store cached objects. Defaults to "cache".
        disabled: whether or not to bypass the cache for the function call. Defaults to False.
        refresh: whether or not to bypass cache lookup to force a new cache write. Defaults to False.
        log_level: level to emit logs at. defaults to INFO
        identifiers: additional arguments that are hashed to identify a unique function call. Defaults to [].
        path_seperators: list of argument names to use as path seperators after `path`
        is_method: whether or not the cached function is an object's method. Defaults to False.
        instance_identifiers: name of instance attributes to include in `identifiers` if `is_method` is `True`. Defaults to [].
        instance_path_seperators: name of instance attributes to include in `path_seperators` if `is_method` is `True`. Defaults to [].
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if os.getenv("PYUTIL_DISABLE_CACHE"):
                return func(*args, **kwargs)

            kwargs = sort_dict(get_full_kwargs(func, kwargs))
            named_args = get_named_args(func, args)

            all_args = {**kwargs, **named_args}

            # Parameters inherited from decorator generator call
            params = {
                "path": path,
                "disabled": disabled,
                "refresh": refresh,
                "log_level": log_level,
                "identifiers": identifiers,
                "path_seperators": path_seperators,
                "is_method": is_method,
                "instance_identifiers": instance_identifiers,
                "instance_path_seperators": instance_path_seperators,
            }

            # Update params using override passed in through calling function
            if "cache_kwargs" in kwargs:
                # Support special cache_kwargs parameter in case calling function has a name clash with cache params
                params.update(kwargs["cache_kwargs"])
                del kwargs["cache_kwargs"]

            else:
                # Since cache_kwargs was not provided, check for overrides directly in kwargs.
                # Note that params get deleted from kwargs so cache_kwargs should be used in case of
                # name conflicts
                params.update(kwargs)

                for key in params.keys():
                    try:
                        # Delete override from function kwargs before passing to query
                        del kwargs[key]
                    except KeyError:
                        pass

            try:
                name = func.__name__
            except AttributeError:
                name = "function"

            # Parse identifiers and path seperators
            if params["is_method"]:
                # remove self argument
                instance = args[0]
                hashable_args = args[1:]
                _identifiers = params["identifiers"] + [getattr(instance, id) for id in params["instance_identifiers"]]
                _path_seperators = [all_args[ps] for ps in params["path_seperators"]] + [
                    getattr(instance, ps) for ps in params["instance_path_seperators"]
                ]
            else:
                hashable_args = args
                _identifiers = params["identifiers"]
                _path_seperators = [all_args[ps] for ps in params["path_seperators"]]

            # Add path seperators
            params["path"] = os.path.join(params["path"], *_path_seperators)

            actual_args = hashable_args
            hashable_args = [*hashable_args, *_identifiers]

            key = hash_item([hash_item(i) for i in [hashable_args, kwargs]])

            _func_kwargs = (f"{k}={v}" for k, v in kwargs.items())
            return Cache(
                params["path"],
                name,
                (
                    *actual_args,
                    *(f"(id:{i})" for i in _identifiers),
                    *_func_kwargs,
                ),
                params["log_level"],
            ).query(
                key,
                func,
                query_fn_args=args,
                query_fn_kwargs=kwargs,
                refresh=params["refresh"],
                disabled=params["disabled"],
            )

        return wrapper

    return decorator
