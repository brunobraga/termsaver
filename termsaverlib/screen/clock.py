###############################################################################
#
# file:     clock.py
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
This module contains a simple screen that displays current time on terminal.
See additional information in the class itself.

The screen class available here is:

    * `ClockScreen`
"""

#
# Python mobdules
#
import datetime
import time

#
# Internal modules
#
from termsaverlib.screen.base import ScreenBase
from termsaverlib.screen.helper.position import PositionHelperBase
from termsaverlib import common
from termsaverlib.i18n import _


class ClockScreen(ScreenBase, PositionHelperBase):
    """
    Simple screen that displays the time on the terminal window.

    The ascii font used was retrieved from Figlet application
    (http://www.figlet.org/).

    From its base classes, the functionality provided here bases on the
    settings defined below:

        * clean up each cycle: True
          this will force the screen to be cleaned (cleared) before each new
          cycle is displayed
    """

    digmap = {
        '0': '  ___  \n / _ \ \n| | | |\n| |_| |\n \___/ \n',
        '1': '   _   \n  / |  \n  | |  \n  | |  \n  |_|  \n',
        '2': ' ____  \n|___ \ \n  __)  \n / __/ \n|_____|\n',
        '3': ' _____ \n|___ / \n  |_ \ \n ___) |\n|____/ \n',
        '4': ' _  _  \n| || | \n| || | \n|__  | \n   |_| \n',
        '5': ' ____  \n| ___| \n|___ \ \n ___) |\n|____/ \n',
        '6': '  __   \n / /_  \n| \'_ \ \n| (_) |\n \___/ \n',
        '7': ' _____ \n|___  |\n   / / \n  / /  \n /_/   \n',
        '8': '  ___  \n ( _ ) \n / _ \ \n| (_) |\n \___/ \n',
        '9': '  ___  \n / _ \ \n| (_) |\n \__, |\n   /_/ \n',
        ':': '       \n   _   \n  (_)  \n   _   \n  (_)  \n',

    }
    """
    Holds the ascii characters to be used by this screen. It is the
    simplification of:
      ___   _  ____   _____  _  _    ____    __    _____   ___    ___
     / _ \ / ||___ \ |___ / | || |  | ___|  / /_  |___  | ( _ )  / _ \  _
    | | | || |  __) |  |_ \ | || |_ |___ \ | '_ \    / /  / _ \ | (_) |(_)
    | |_| || | / __/  ___)  |__   _| ___) || (_) |  / /  | (_) | \__, | _
     \___/ |_||_____||____/    |_|  |____/  \___/  /_/    \___/    /_/ (_)

    Extracted from standard font of Figlet (http://www.figlet.org/)
    """

    def __init__(self):
        """
        The constructor of this class.
        """
        ScreenBase.__init__(self,
            "clock",
            _("displays a digital clock on screen"),
            {'opts': 'h', 'long_opts': ['help']},
        )
        self.cleanup_per_cycle = True

    def _run_cycle(self):
        """
        Executes a cycle of this screen.
        """
        # calculate random position based on screen size
        self.get_terminal_size()

        date_time = datetime.datetime.now()

        text = """
%s
%s
""" % (
       date_time.strftime('%A, %%d%%s %B %Y') % (date_time.day,
                common.get_day_suffix(date_time.day)),
       self.get_ascii_time(date_time),
       )

        text = self.center_text_horizontally(text)
        text = self.center_text_vertically(text)

        print text

        time.sleep(1)

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

 -h, --help   Displays this help message

""")

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

    def get_ascii_time(self, date_time):
        """
        Returns the ASCII representation of a date.
        """
        clock = date_time.strftime('%H:%M:%S')
        items = []
        for c in clock:
            items.append(self.digmap[c])
        output = ''
        for i in range(5):  # loop lines of chars
            temp = ''
            for item in items:
                temp += item.split('\n')[i]
            output += temp + '\n'

        return output
