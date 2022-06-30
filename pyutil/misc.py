import inspect

def get_full_kwargs(func, kwargs) -> dict:
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

def get_named_args(func, args) -> dict:
    """Return `func`'s arguments as a dictionary with keys as the argument names as defined in `func`
    
    Example:
    >>> def a(a, b, c):
    >>>     return a + b + c

    >>> get_named_args(a, (5, 6, 7))
    {"a": 5, "b": 6, "c": 7}
    """
    arg_names = [k for k, v in inspect.signature(func).parameters.items() if v.kind == v.POSITIONAL_OR_KEYWORD and v.default == v.empty]
    return dict(zip(arg_names, args))
    