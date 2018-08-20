# -*- coding: utf-8 -*-

# $Id:$

"""This modules defines the plugin API.

"""

import pluggy

from .common import PROJECT_NAME

hookspec = pluggy.HookspecMarker(PROJECT_NAME)


@hookspec
def initialize():
    """Initialize the plugin.

    Function called when djira app is initialized (method ``ready``).
    A plugin can implement this hook if it requires some
    initialization.

    """


@hookspec
def get_endpoints():
    """Returns the endpoints defined by the plugin.

    Returns a list of ``EndPoint`` instances.

    """
