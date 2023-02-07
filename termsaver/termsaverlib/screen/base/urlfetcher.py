###############################################################################
#
# file:     urlfetcher.py
#
# Purpose:  refer to module documentation for details
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
This module contains a screen base class that handles URL fetched contents.
See additional information in the class itself.

The helper classes available here are:

    * `UrlFetcherBase`
    * `SimpleUrlFetcherBase`
"""

from termsaver.termsaverlib import constants, exception
from termsaver.termsaverlib.i18n import _
#
# Internal modules
#
from termsaver.termsaverlib.screen.base import ScreenBase
from termsaver.termsaverlib.screen.helper.typing import TypingHelperBase
from termsaver.termsaverlib.screen.helper.urlfetcher import \
    URLFetcherHelperBase


class UrlFetcherBase(TypingHelperBase,
                     URLFetcherHelperBase):
    """
    A base class used to handle URL fetched contents, and display them
    accordingly. This also includes the `TypingHelperBase` to add functionality
    of typing writer display.

    The instantiation of this class takes two additional arguments, compared
    with its base class:

        * url: the URL address to fetch data from

        * `delay`: defines the delay for printing out characters of
           a string
    """

    url = ""
    """
    the URL address to fetch data from
    """
    def __init__(self, parser, url=None, delay=None):
        """
        Creates a new instance of this class.

        This constructor has two additional arguments, compared with its base
        class:

            * url: the URL address to fetch data from

            * `delay`: defines the delay for printing out characters of
               a string
       """
        if self.parser:
            self.parser.add_argument("-d","--delay", action="store", type=int, help="""Sets the speed of the displaying characters
                    default is%(default_delay)s of a second""" % {'default_delay': constants.Settings.CHAR_DELAY_SECONDS})

        self.delay = delay
        self.url = url
        self.parser = parser

    def _run_cycle(self):
        """
        Executes a cycle of this screen.

        The actions taken here, for each cycle, are as follows:

            * retrieve data from `url`
            * print using `typing_print`
        """
        data = self.fetch(self.url)
        self.clear_screen()
        self.typing_print(data.decode("utf-8"))

    def _message_no_url(self):
        """
        Defines a method to be overriden by inheriting classes, with the
        purpose to display extra help information for specific errors.
        """
        return ""

    def _parse_args(self, launchScreenImmediately=True):
        """
        Handles the special command-line arguments available for this screen.
        Although this is a base screen, having these options prepared here
        can save coding for screens that will not change the default options.

        See `_usage_options_example` method for documentation on each of the
        options being parsed here.

        Additionally, this is dependent on the values exposed in `cli_opts`,
        passed to this class during its instantiation. Only values properly
        configured there will be accepted here.
        """
        args,unknown = self.parser.parse_known_args()
        if args.delay:
            try:
                self.delay = float(args.delay)
            except:
                raise exception.InvalidOptionException("delay")

        if args.url:
            try:
                self.url = self.fix_uri(args.url)
            except Exception as e:
                error_message = ""
                if hasattr(e, 'message'):
                    error_message = e.message
                else:
                    error_message = e
                raise exception.InvalidOptionException("url", error_message)

        # last validations
        if self.url in (None, ''):
            raise exception.InvalidOptionException("url",
                _("It is mandatory option"), help=self._message_no_url())
        
        if launchScreenImmediately:
            self.autorun()
        else:
            return self


class SimpleUrlFetcherBase(ScreenBase, UrlFetcherBase):
    """
    Inherits the `UrlFetcherBase` class to handle basic URL fetching.
    This will simplify the use of UrlFetcherBase by forcing a fixed
    URL, and simplify the code of screens inheriting from it.
    """

    def __init__(self, name, description, parser, url, delay=None):
        """
        Creates a new instance of this class.

        This constructor has forced the url argument, compared with its base
        class, as it has no command line options to define its value manually
        """
        ScreenBase.__init__(self, name, description, parser)
        UrlFetcherBase.__init__(self, parser, url, delay)

    
    def _run_cycle(self):
        UrlFetcherBase._run_cycle(self)
