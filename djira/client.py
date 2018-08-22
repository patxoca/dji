# -*- coding: utf-8 -*-

# $Id:$

"""Python djira's client.

This module serves both as an example for client implementers and as a
test for the API usability from the client perspective.

"""

from __future__ import print_function
from __future__ import unicode_literals

import json
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import urlopen


class _Proxy(object):

    # NOTE: I use slots as a way to discourege tinkering with the
    # instance state. Once instantiated a proxy must be considered
    # read-only so that it can be reused.
    __slots__ = ("_url", "_endpoint", "_full_url", "_url_opener")

    def __init__(self, url, endpoint, url_opener=urlopen):
        if not url.endswith("/"):
            url = url + "/"
        if not endpoint.endswith("/"):
            endpoint = endpoint + "/"
        self._url = url
        self._endpoint = endpoint
        self._full_url = url + endpoint
        self._url_opener = url_opener

    def __call__(self, **kwargs):
        url = self._make_url(self._full_url, kwargs)
        try:
            return self._read_from_url(url, self._url_opener)
        except HTTPError as e:
            # HACK: log instead of printing
            print("HTTPError, status {}".format(e.code))
            return None  # HACK: must raise some exception
        except URLError as e:
            print("URLError, reason {}".format(e.reason))
            return None

    @staticmethod
    def _make_url(url, param_dict):
        if param_dict:
            # TODO: test with non ASCII input
            qs = urlencode(list(param_dict.items()), doseq=True)
            url = url + "?" + qs  # HACK: that don't look good
        return url

    @staticmethod
    def _read_from_url(url, opener):
        with opener(url) as response:
            if response.status != 200:
                raise RuntimeError("status != 200: {}".format(response.status))
            if response.getheader("Content-Type") != "application/json":
                raise RuntimeError(
                    "unsupported content-type: '{}'".format(
                        response.getheader("Content-Type")
                    )
                )
            return json.loads(response.read())


class DjiraClient(object):

    MIN_API_VERSION_SUPPORTED = (1, 0)

    def __init__(self, url):
        self.url = url
        self._proxies = {}

    def __getattr__(self, name):
        if name not in self._proxies:
            self._proxies[name] = _Proxy(self.url, name)
        return self._proxies[name]

    def check_minimum_api_version(self):
        version = tuple(self.__version__())
        return self.MIN_API_VERSION_SUPPORTED <= version
