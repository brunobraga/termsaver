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

#
# Internal modules
#
from termsaverlib.screen.base import ScreenBase
from termsaverlib import exception, constants
from termsaverlib.screen.helper.urlfetcher import URLFetcherHelperBase
from termsaverlib.screen.helper.typing import TypingHelperBase
from termsaverlib.i18n import _


class UrlFetcherBase(ScreenBase,
                     TypingHelperBase,
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

    def __init__(self, name, description, url=None,
                 delay=None, cli_opts=None):
        """
        Creates a new instance of this class.

        This constructor has two additional arguments, compared with its base
        class:

            * url: the URL address to fetch data from

            * `delay`: defines the delay for printing out characters of
               a string
       """
        ScreenBase.__init__(self, name, description, cli_opts)
        if not cli_opts:
            self.cli_opts = {
                             'opts': 'hd:u:',
                             'long_opts': ['help', 'delay=', 'url='],
            }
        self.delay = delay
        self.url = url

    def _run_cycle(self):
        """
        Executes a cycle of this screen.

        The actions taken here, for each cycle, are as follows:

            * retrieve data from `url`
            * print using `typing_print`
        """
        data = self.fetch(self.url)
        self.clear_screen()
        self.typing_print(data)

    def _message_no_url(self):
        """
        Defines a method to be overriden by inheriting classes, with the
        purpose to display extra help information for specific errors.
        """
        return ""

    def _usage_options_example(self):
        """
        Describe here the options and examples of this screen.

        The method `_parse_args` will be handling the parsing of the options
        documented here.

        Additionally, this is dependent on the values exposed in `cli_opts`,
        passed to this class during its instantiation. Only values properly
        configured there will be accepted here.
        """
        print _("""
Options:

 -u, --url    Defines the URL location from where the information
              should be fetched, then displayed.
              This option is MANDATORY.
 -d, --delay  Sets the speed of the displaying characters
              default is 0.003 of a second (advised to keep
              between 0.01 and 0.001).
 -h, --help   Displays this help message

Examples:

    $ %(app_name)s %(screen)s -u www.google.com
    This will trigger the screensaver to fetch the HTML contents of this web
    site and display progressively.

    $ %(app_name)s %(screen)s -u www.google.com -d 0
    This will trigger the screensaver to fetch the HTML contents of this web
    site with no delay (too fast for a screensaver, but it's your choice that
    matters!)
""") % {
        'screen': self.name,
        'app_name': constants.App.NAME,
    }

    def _parse_args(self, prepared_args):
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
        for o, a in prepared_args[0]:  # optlist, args
            if o in ("-h", "--help"):
                self.usage()
                self.screen_exit()
            elif o in ("-d", "--delay"):
                try:
                    # make sure argument is a valid value (float)
                    self.delay = float(a)
                except:
                    raise exception.InvalidOptionException("delay")
            elif o in ("-u", "--url"):
                try:
                    # try to fix the url formatting
                    self.url = self.fix_uri(a)
                except Exception, e:
                    raise exception.InvalidOptionException("url", e.message)
            else:
                # this should never happen!
                raise Exception(_("Unhandled option. See --help for details."))

        # last validations
        if self.url in (None, ''):
            raise exception.InvalidOptionException("url",
                _("It is mandatory option"), help=self._message_no_url())


class SimpleUrlFetcherBase(UrlFetcherBase):
    """
    Inherits the `UrlFetcherBase` class to handle basic URL fetching.
    This will simplify the use of UrlFetcherBase by forcing a fixed
    URL, and simplify the code of screens inheriting from it.
    """

    def __init__(self, name, description, url, delay=None):
        """
        Creates a new instance of this class.

        This constructor has forced the url argument, compared with its base
        class, as it has no command line options to define its value manually
        """
        UrlFetcherBase.__init__(self, name, description, url, delay,
                            {'opts': 'h', 'long_opts': ['help']})

    def _usage_options_example(self):
        """
        Describe here the options and examples of this screen.

        The method `_parse_args` will be handling the parsing of the options
        documented here.

        Additionally, this is dependent on the values exposed in `cli_opts`,
        passed to this class during its instantiation. Only values properly
        configured there will be accepted here.
        """
        print """
Options:

 -h, --help   Displays this help message
"""

    def _parse_args(self, prepared_args):
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
        for o, __ in prepared_args[0]:  # optlist, args
            if o in ("-h", "--help"):
                self.usage()
                self.screen_exit()
            else:
                # this should never happen!
                raise Exception(_("Unhandled option. See --help for details."))
