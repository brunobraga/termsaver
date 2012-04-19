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
available within any plugins installed. Available functions:

    * `get_available_plugin_screens`: Gets the available screens in
       sub-directories {plugin}/screen/ for dynamic instantiation.

The modules available in this package are installed on-demand, so they are
not documented here.

How to create plugins
=====================

The main script termsaver will execute a dynamic search for all screens
that inherit from the `ScreenBase` class. For plugins, however, screens are
not placed in the same directory of the built-in screens, but instead into
their own location.

The directory structure of a plugin should be like:

      plugins/
         |
         |---- __init__.py
         |
         |---- my_plugin/
         |         |
         |         |---- __init__.py
         |         |
         |         |---- screen
         |         |       |
         |         |       |---- __init__.py
         |         |       |
         |         |       |---- my_screen.py
         |         |       |
         |         |       |---- ...
         |         |       |

Additional rules before you begin:

(1) Naming Conventions
    The application name must be in the format: termsaver-{plugin-name}, and
    the directory to be created inside the plugins will be {plugin-name}.

    Python does not like dashes for module names, so be careful with names you
    pick.

(2) Screens
    Each screen you design (inside the plugins/{plugin-name}/screen directory)
    must inherit from the `ScreenBase` class, as this is the base for the
    application to find the screen, and handle input/output accordingly.


This sctructure is designed to immitate termsaver's main structure, so once you
get familiar with it, it should be piece of cake to manage your own "space".

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


def get_available_plugin_screens():
    """
    Gets the available screens in this package for dynamic instantiation.
    """
    ignore_list = ['__init__.py']
    screens = []
    for plugin in os.listdir(os.path.join(os.path.dirname(__file__))):
        if (os.path.isdir(os.path.join(os.path.dirname(__file__), plugin))):
            # we are inside the plugin directory, get screens available in
            # screens directory
            for module in os.listdir(os.path.join(os.path.dirname(__file__),
                    plugin, "screen")):
                if module in ignore_list or module[-3:] != '.py':
                    continue
                module_name = plugin + ".screen." + module[:-3]

                m = __import__(module_name, globals(), locals(),
                        [module_name.rsplit(".", 1)[-1]])

                # loop module's classes in search for the ones inheriting
                # Screenbase and ignore name (no need) with underscore variable
                for name, obj in inspect.getmembers(m):
                    if inspect.isclass(obj) and issubclass(obj,
                            base.ScreenBase) and not name.endswith("Base"):
                        screens.append(obj)
    return screens
