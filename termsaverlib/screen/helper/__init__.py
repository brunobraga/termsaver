###############################################################################
#
# file:     __init__.py
#
# Purpose:  refer to package documentation for details
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
This package holds all helper classes used by termsaver screens, to add
reusable functionality to them, and help maintain consistency throughout all
of them.

All helper screens should inherit from the base screen helper
`ScreenHelperBase`, documented below.

The available classes in this package are:

    * `ScreenHelperBase`: the main helper class from which all helper classes
      will inherit from.

    * `typing.TypingHelperBase`: helper functionality to display typing writer
      effects for screens.

    * `urlfetcher.URLFetcherHelperBase`: helper functionalities to give
      Internet connectivity to screens.

    * `xmlreader.XMLReaderHelperBase`: helper functionalities to assist on
       XML parsing.

"""
#
# Python built-in modules
#
from os import system

#
# Internal modules
#
from termsaverlib.common import is_windows


class ScreenHelperBase(object):
    """
    This is the main helper class from which all should inherit from. This
    will also hold most rudimentary functionalities that can be reused by
    all screens.
    """

    @staticmethod
    def clear_screen():
        """
        A simple method that clears the screen.

        This supports both Windows and Unix base systems.
        """
        if is_windows():
            # Execute command for Windows Platform, DOS console
            __ = system('cls')  # Windows prints the output of this call
        else:
            # Execute command for Unix based Platform
            system('clear')
