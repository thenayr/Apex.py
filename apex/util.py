import json
import random

import requests

userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"


def GET(url: str, headers={}):
    """
    Return the response of an HTTP GET request to the specified URL with
    the provided header values.

    Defaults to Google Chrome user agent and disallowed redirects.
    """

    # Allow custom user agent when needed.
    if "User-Agent" not in headers:
        headers["User-Agent"] = userAgent

    return requests.get(url, headers=headers, allow_redirects=False)


def POST(url: str, headers={}, data=None):
    """
    Return the response of an HTTP POST request to the specified URL
    with the provided header values.

    Defaults to Google Chrome user agent.
    """

    # Allow custom user agent when needed.
    if "User-Agent" not in headers:
        headers["User-Agent"] = userAgent

    return requests.post(url, headers=headers, data=data)


def GenerateCID(length: int):
    """
    Return a randomly generated alphanumerical string of the specified
    length.
    """

    charSet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

    return "".join([random.choice(charSet) for _ in range(length)])


def ReplaceAll(data: str, keys: dict):
    """ToDo"""

    for old, new in keys.items():
        data = data.replace(old, f"\"{new}\"")

    return data
