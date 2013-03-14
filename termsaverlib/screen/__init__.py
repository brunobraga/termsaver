###############################################################################
#
# file:     __init__.py
#
# Purpose:  refer to python doc for documentation details.
#
# Note:     This file is part of Termsaver application, and should not be used
#           or executed separately.
#
###############################################################################
#
# Copyright 2012 Termsaver
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
###############################################################################
"""
This module itself holds simple functions to better handle the screens
available within this package. Available functions:

    * `get_available_screens`: Gets the available screens in this package for
       dynamic instantiation.

    * `build_screen_usage_list`: Builds a simple string with a list of all
       available screens, to be used in usage() methods.

The modules available in this package are:

    * `asciiartfarts`: displays ascii images from asciiartfarts.com

    * `clock`: displays a digital clock

    * `sysmon`: displays a graphic for CPU/Mem usage

    * `jokes4all`: displays recent jokes from jokes4all.net

    * `programmer`: displays source code in typing animation

    * `quotes4all`: displays recent quotes from quotes4all.net

    * `randtxt`: displays word in random places on screen

    * `rfc`: randomly displays RFC contents

    * `rssfeed`: displays rss feed information

    * `urlfetcher`: displays url contents with typing animation

    * `matrix`: displays a matrix movie alike screensaver

This also contains the following sub-packages:

    * `base`: holds base classes that are used by all screens within termsaver
       application

    * `helper`: holds all helper classes used by termsaver screens, to add
       reusable functionality to them
"""

#
# Python built-in modules
#
import os
import inspect

#
# Internal modules
#
from termsaverlib.screen import base
from termsaverlib.plugins import get_available_plugin_screens


def get_available_screens():
    """
    Gets the available screens in this package for dynamic instantiation.
    """
    ignore_list = ['__init__.py']
    screens = []
    for module in os.listdir(os.path.join(os.path.dirname(__file__))):
        if module in ignore_list or module[-3:] != '.py':
            continue
        module_name = module[:-3]
        m = __import__(module_name, globals(), locals())

        # loop module's classes in search for the ones inheriting Screenbase
        # and ignore name (no need) with underscore variable
        for name, obj in inspect.getmembers(m):
            if inspect.isclass(obj) and issubclass(obj, base.ScreenBase) \
                    and not name.endswith("Base"):
                screens.append(obj)

    # find plugins
    screens.extend(get_available_plugin_screens())

    return screens


def build_screen_usage_list():
    """
    Builds a simple string with a list of all available screens,
    to be used in usage() methods.
    """
    screens = get_available_screens()
    screen_space = max([len(s().name) for s in screens])

    return '\n '.join([''.join([s().name, ' ',
                        ' ' * (screen_space - len(s().name) + 1),
                        s().description]) for s in get_available_screens()])
