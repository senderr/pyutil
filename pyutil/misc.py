import inspect


def get_full_kwargs(func, kwargs):
    """Return `func`'s fallback kwargs + explicit kwargs combined"""

    default_kwargs = {
        k: v.default for k, v in inspect.signature(func).parameters.items() if v.default is not inspect.Parameter.empty
    }
    default_kwargs.update(kwargs)
    return default_kwargs
