from collections.abc import Mapping
from typing import Any, Callable

def add_namespace(data:dict, ns: str|None)->dict:
    if not ns:
        return dict(data)
    else:
        return {(k if ':' in k else f"{ns}:{k}"): v for k, v in data.items()}


def traverse(data:dict|Any, fn=Callable)->dict:
    if not isinstance(data, Mapping):
        return data
    new_data = {}
    for k, v in fn(data).items():
        new_data[k] = traverse(v, fn)
    return new_data