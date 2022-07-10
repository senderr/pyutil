def stack_dict(d, path=[]) -> list:
    """Return a list, where each element is a list of the dict key path required to reach val, followed by val
    Example:
    >>> stack_dict({'a': {'b': {'c': 1}}, 'd': 2})
    >>> [['a', 'b', 'c', 1], ['d', 2]]

    Args:
        d (dict): The dict to stack

    Returns:
        list: stacked dict
    """
    res = []
    for k, v in d.items():
        if isinstance(v, dict):
            res.extend(stack_dict(v, path + [k]))
        else:
            res.append(path + [k, v])
    return res


def sort_dict(d, reverse=False) -> dict:
    """Sort a dict based on keys recursively"""
    new_d = {}
    sorted_keys = sorted(d, reverse=reverse)
    for key in sorted_keys:
        if isinstance(d[key], dict):
            new_d[key] = sort_dict(d[key])
        else:
            new_d[key] = d[key]
    return new_d


def format_dict(dict_, ind="    ", trail="_"):
    """Return string representation of dict with correct indentation"""
    out = "{\n"
    n = max(len(str(x)) for x in dict_.keys())
    for k, v in dict_.items():
        out += ind + f"{k}:".ljust(n + 2, trail)
        if isinstance(v, dict):
            out += "{ \n" + format_dict(v, ind + "    ")
        else:
            out += str(v) + "\n"

    if len(ind) > 0:
        out += "}\n"
    return out
