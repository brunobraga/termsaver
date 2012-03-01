###############################################################################
#
# file:     dot.py
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
This module contains a simple screen that displays a running dot on terminal.
See additional information in the class itself.

The screen class available here is:

    * `DotScreen`
"""

#
# Python mobdules
#
import random
import time

#
# Internal modules
#
from termsaverlib.screen.base import ScreenBase
from termsaverlib.screen.helper.position import PositionHelperBase
from termsaverlib import constants, exception
from termsaverlib.i18n import _


class DotScreen(ScreenBase, PositionHelperBase):
    """
    Simple screen that displays a running (animation) dot on a terminal window.

    From its base classes, the functionality provided here bases on the
    settings defined below:

        * clean up each cycle: True
          this will force the screen to be cleaned (cleared) before each new
          cycle is displayed
    """

    def __init__(self):
        """
        The constructor of this class.
        """
        ScreenBase.__init__(self,
            "dot",
            _("displays a random running dot"),
            {'opts': 'hc:d:', 'long_opts': ['help', 'char=', 'delay=']},
        )
        self.char = "*"
        self.text = ""
        self.size = 1
        self.delay = 0.05
        self.cleanup_per_cycle = True

    def _run_cycle(self):
        """
        Executes a cycle of this screen.
        """
        # calculate random position based on screen size
        self.get_terminal_size()

        if len(self.text) == 0:
            self.text = self.char
        if self.pos_x in (self.screen_width - len(self.text),
                self.screen_width):
            self.pos_x = 1
            self.pos_y = random.randint(1, self.screen_height)

            # change char size randomly
            if (len(self.text) > 1 or len(self.text) == self.screen_width) \
                    and random.random() < 0.5:
                self.text = self.text[:-1]  # remove trailing char
            else:
                self.text += self.char  # add char

        self.pos_x += 1

        txt = "\n" * self.pos_y + " " * self.pos_x + self.text \
             + " " * (self.screen_width - self.pos_x - len(self.text))

        # just print the whole text
        print txt

        time.sleep(self.delay)

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

 -c, --char   Sets the character to be showing up
              default is X
 -d, --delay  Sets the speed of the displaying characters
              default is 0.05 of a second (advised to keep
              between 0.1 and 0.01).
 -h, --help   Displays this help message

Example:

    $ %(app_name)s %(screen)s
    This will trigger the screensaver to display a dot on screen, with random
    size increase.

    $ %(app_name)s %(screen)s -c +
    Overrides the default dot (.) character to be a plus sign (+)

""") % {
        'app_name': constants.App.NAME,
        'screen': self.name,
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
            elif o in ("-c", "--char"):
                # make sure argument is a valid value (single char)
                if len(a) != 1:
                    raise exception.InvalidOptionException("char")
                else:
                    self.char = a
            else:
                # this should never happen!
                raise Exception(_("Unhandled option. See --help for details."))
