###############################################################################
#
# file:     randtxt.py
#
# Purpose:  holds base classes used by screens in termsaver
#           refer to module documentation for details
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
Simple screensaver that displays a text in random position on screen.

See additional information in the class itself.

The screen class available here is:

    * `RandTxtScreen`
"""

import time

from termsaverlib.screen.base import ScreenBase
from termsaverlib.screen.helper.typing import TypingHelperBase
from termsaverlib.screen.helper.position import PositionHelperBase
from termsaverlib import constants, exception
from termsaverlib.i18n import _


class RandTxtScreen(ScreenBase,
                    TypingHelperBase,
                    PositionHelperBase):
    """
    Simple screensaver that displays a text in random position on screen.

    This screen offers the additional options to customize its behavior:

        * `delay`: Defines the freezing time for a word to be displayed on
          screen, before a next randomization (cycle). If never changed by
          command-line options, it will assume the value of `FREEZE_WORD_DELAY`

        * `word`: defines the word to be displayed on screen
          for files
    """

    word = ''
    """
    Holds the word to be displayed on screen
    """

    freeze_delay = 0
    """
    Defines the freezing time for a word to be displayed on screen, before a
    next randomization (cycle). If never changed by command-line options,
    it will assume the value of `FREEZE_WORD_DELAY`.
    """

    FREEZE_WORD_DELAY = 3
    """
    A default freezing time for a word to be displayed on screen, before a
    next randomization (cycle). Its value is set to 3 seconds.
    """

    def __init__(self):
        """
        Creates a new instance of this class.
        """
        ScreenBase.__init__(self,
            "randtxt",
            _("displays word in random places on screen"),
            {'opts': 'hw:d:', 'long_opts': ['help', 'word=', 'delay=']},
        )
        self.word = constants.App.TITLE
        self.delay = 0.01
        self.line_delay = 0
        self.cleanup_per_cycle = True
        self.freeze_delay = self.FREEZE_WORD_DELAY

    def _run_cycle(self):
        """
        Executes a cycle of this screen.

        The actions taken here, for each cycle, are as follows:

            * randomize text position vertically and horizontally
            * print using `typing_print`
        """
        # calculate random position based on screen size
        self.get_terminal_size()

        txt = self.randomize_text_vertically(
            self.randomize_text_horizontally(self.word))

        self.typing_print(txt)

        time.sleep(self.freeze_delay)

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

 -w, --word   Sets the word to be displayed
              default is the name of this application (if you need to use
              spaces, don't forget to place the word with quotes)
 -d, --delay  Sets how long the word will be displayed before
              randomized again. Default is %(default_delay)s second(s)
 -h, --help   Displays this help message

Example:

    $ %(app_name)s %(screen)s
    This will trigger the screensaver to display the default word %(app_title)s
    in random locations of the screen

    $ %(app_name)s %(screen)s -w FooBar
    This will trigger the screensaver to display the default word FooBar
    in random locations of the screen
""") % {
        'app_name': constants.App.NAME,
        'app_title': constants.App.TITLE,
        'screen': self.name,
        'default_delay': self.FREEZE_WORD_DELAY,
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
                    self.freeze_delay = float(a)
                except:
                    raise exception.InvalidOptionException("delay")
            elif o in ("-w", "--word"):
                # make sure argument is a valid value
                if a in (None, ''):
                    raise exception.InvalidOptionException("word")
                self.word = a
            else:
                # this should never happen!
                raise Exception(_("Unhandled option. See --help for details."))
