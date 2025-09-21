#!/usr/bin/env python3
"""
Utility functions for unit testing exercises.

Includes:
- access_nested_map: retrieves values from nested dictionaries
- get_json: fetches JSON payload from a URL
- memoize: caches method results
"""

from typing import Any, Dict, Tuple
import requests
from functools import wraps


def access_nested_map(nested_map: Dict, path: Tuple) -> Any:
    """
    Access a nested map and return the value at the end of the path.

    Args:
        nested_map (dict): The dictionary to access.
        path (tuple): Sequence of keys to traverse.

    Returns:
        Any: Value found at the specified path.

    Raises:
        KeyError: If a key in the path does not exist.
    """
    current = nested_map
    for key in path:
        if key not in current:
            raise KeyError(key)
        current = current[key]
    return current


def get_json(url: str) -> Dict:
    """
    Fetch JSON content from a URL using HTTP GET.

    Args:
        url (str): The URL to fetch.

    Returns:
        dict: JSON payload from the response.
    """
    response = requests.get(url)
    return response.json()


def memoize(method):
    """
    Decorator to cache a method's result as a property.

    Args:
        method (Callable): Method to memoize.

    Returns:
        property: Cached property.
    """
    attr_name = f"_{method.__name__}_cached"

    @property
    @wraps(method)
    def memoized(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self))
        return getattr(self, attr_name)

    return memoized
