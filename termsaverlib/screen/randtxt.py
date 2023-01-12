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

    def __init__(self, parser = None):
        """
        Creates a new instance of this class.
        """
        ScreenBase.__init__(self,
            "randtxt",
            _("displays word in random places on screen"),
            parser
        )
        if self.parser:
            self.parser.add_argument("-w", "--word", type=str, required=False, help="The words to randomly display on screen.")
            self.parser.add_argument("-d", "--delay", type=float, required=False, default=self.freeze_delay, help="The delay between changing words.")
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
        print (_("""
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
       })

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
                # make sure argument is a valid value (float)
                self.freeze_delay = float(args.delay)
            except:
                raise exception.InvalidOptionException("delay")
        if args.word:
            if args.word in (None, ''):
                raise exception.InvalidOptionException("word")
            self.word = args.word

        if launchScreenImmediately:
            self.autorun()
        else:
            return self
