# 0x03-Unittests_and_integration_tests/utils.py
#!/usr/bin/env python3
"""
Utility functions module
"""

import requests
from functools import wraps
from typing import Any, Dict, List, Union, Mapping, Sequence


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """
    Access nested map with key path
    """
    for key in path:
        if not isinstance(nested_map, Mapping):
            raise KeyError(key)
        nested_map = nested_map[key]
    return nested_map


def get_json(url: str) -> Dict:
    """
    Get JSON from remote URL
    """
    response = requests.get(url)
    return response.json()


def memoize(func):
    """
    Memoize decorator
    """
    attr_name = "_{}".format(func.__name__)

    @wraps(func)
    def memoized(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, func(self))
        return getattr(self, attr_name)

    return property(memoized)