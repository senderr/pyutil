import inspect


def get_full_kwargs(func, kwargs):
    """Return `func`'s fallback kwargs + explicit kwargs combined

    Example:
    >>> def a(b=1, c=2):
    >>>     return b + c

    >>> get_full_kwargs(a, {})
    {'b': 1, 'c': 2}
    """

    default_kwargs = {
        k: v.default for k, v in inspect.signature(func).parameters.items() if v.default is not inspect.Parameter.empty
    }
    default_kwargs.update(kwargs)
    return default_kwargs
