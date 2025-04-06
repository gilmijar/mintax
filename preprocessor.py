from typing import Any, Callable


def get_namespace(whence: str) -> str | None:
    """Extracts the namespace from a colon-delimited string."""
    return whence.rpartition(':')[0]


def add_namespace(data: dict, ns: str | None) -> dict:
    """Applies a namespace prefix to keys that lack one."""
    if not ns:
        return dict(data)
    else:
        return {
            (k if ':' in k else f"{ns}:{k}"): v
            for k, v
            in data.items()
        }


def namespace_traverse(data: dict | Any, fn: Callable, ns: str | None = None) -> dict:
    """Recursively apply a function to a nested dictionary structure, maintaining namespace context."""
    if not isinstance(data, dict):
        return data
    new_data = {}
    for k, v in fn(data, ns).items():
        _ns = get_namespace(k)
        new_data[k] = namespace_traverse(v, fn, _ns)
    return new_data
