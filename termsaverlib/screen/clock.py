# -*- coding: utf-8 -*-
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

from termsaverlib.helper.smartformatter import SmartFormatter
import argparse


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

    ampm = False
    """
    Defines the format of the datetime to be displayed.
    """

    big = False
    """
    Defines the format of the datetime to be displayed.
    """

    cseparator = ":"
    """
    Do not change this (if you do, change also its ASCII representation)
    """

    show_separator = True
    """
    Defines if the clock separator should be displayed
    """

    lineindigimap = 6

    digmap = {
        '0': '  ___  \n / _ \\ \n| | | |\n| |_| |\n \\___/ \n       \n',
        '1': '   _   \n  / |  \n  | |  \n  | |  \n  |_|  \n       \n',
        '2': ' ____  \n|___ \\ \n  __) |\n / __/ \n|_____|\n       \n',
        '3': ' _____ \n|___ / \n  |_ \\ \n ___) |\n|____/ \n       \n',
        '4': ' _  _  \n| || | \n| || | \n|__  | \n   |_| \n       \n',
        '5': ' ____  \n| ___| \n|___ \\ \n ___) |\n|____/ \n       \n',
        '6': '  __   \n / /_  \n| \'_ \\ \n| (_) |\n \\___/ \n       \n',
        '7': ' _____ \n|___  |\n   / / \n  / /  \n /_/   \n       \n',
        '8': '  ___  \n ( _ ) \n / _ \\ \n| (_) |\n \\___/ \n       \n',
        '9': '  ___  \n / _ \\ \n| (_) |\n \\__, |\n   /_/ \n       \n',
        ':': '       \n   _   \n  (_)  \n   _   \n  (_)  \n       \n',
        'm': '       \n _ _ _ \n|     |\n| | | |\n|_|_|_|\n       \n',
        'p': '       \n _ __  \n| `_ \\ \n| |_) |\n| .__/ \n|_|    \n',
        'a': '       \n  __ _ \n / _` |\n| (_| |\n \\__,_|\n       \n',
        ' ': '       \n       \n       \n       \n       \n       \n',
    }
    """
    Holds the ascii characters to be used by this screen. It is the
    simplification of:
      ___   _  ____   _____  _  _    ____    __    _____   ___    ___
     / _ \ / ||___ \ |___ / | || |  | ___|  / /_  |___  | ( _ )  / _ \  _   _ _ _   _ __     __ _
    | | | || |  __) |  |_ \ | || |_ |___ \ | '_ \    / /  / _ \ | (_) |(_) |     | | `_ \   / _` |
    | |_| || | / __/  ___)  |__   _| ___) || (_) |  / /  | (_) | \__, | _  | | | | | |_) | | (_| |
     \___/ |_||_____||____/    |_|  |____/  \___/  /_/    \___/    /_/ (_) |_|_|_| | .__/   \__,_|
                                                                                   |_|

    Extracted from standard font of Figlet (http://www.figlet.org/)
    """
    digimapbig = {
        '1' : '   ███     \n   ███     \n   ███     \n██████     \n██████     \n██████     \n   ███     \n   ███     \n   ███     \n   ███     \n   ███     \n   ███     \n█████████  \n█████████  \n█████████  \n',
        '2' : '█████████  \n█████████  \n█████████  \n      ███  \n      ███  \n      ███  \n█████████  \n█████████  \n█████████  \n███        \n███        \n███        \n█████████  \n█████████  \n█████████  \n',
        '3' : '█████████  \n█████████  \n█████████  \n      ███  \n      ███  \n      ███  \n   ██████  \n   ██████  \n   ██████  \n      ███  \n      ███  \n      ███  \n█████████  \n█████████  \n█████████  \n',
        '4' : '███   ███  \n███   ███  \n███   ███  \n███   ███  \n███   ███  \n███   ███  \n█████████  \n█████████  \n█████████  \n      ███  \n      ███  \n      ███  \n      ███  \n      ███  \n      ███  \n',
        '5' : '█████████  \n█████████  \n█████████  \n███        \n███        \n███        \n█████████  \n█████████  \n█████████  \n      ███  \n      ███  \n      ███  \n█████████  \n█████████  \n█████████  \n',
        '6' : '█████████  \n█████████  \n█████████  \n███        \n███        \n███        \n█████████  \n█████████  \n█████████  \n███   ███  \n███   ███  \n███   ███  \n█████████  \n█████████  \n█████████  \n',
        '7' : '█████████  \n█████████  \n█████████  \n      ███  \n      ███  \n      ███  \n      ███  \n      ███  \n      ███  \n      ███  \n      ███  \n      ███  \n      ███  \n      ███  \n      ███  \n',
        '8' : '█████████  \n█████████  \n█████████  \n███   ███  \n███   ███  \n███   ███  \n█████████  \n█████████  \n█████████  \n███   ███  \n███   ███  \n███   ███  \n█████████  \n█████████  \n█████████  \n',
        '9' : '█████████  \n█████████  \n█████████  \n███   ███  \n███   ███  \n███   ███  \n█████████  \n█████████  \n█████████  \n      ███  \n      ███  \n      ███  \n█████████  \n█████████  \n█████████  \n',
        '0' : '█████████  \n█████████  \n█████████  \n███   ███  \n███   ███  \n███   ███  \n███   ███  \n███   ███  \n███   ███  \n███   ███  \n███   ███  \n███   ███  \n█████████  \n█████████  \n█████████  \n',
        ':' : '     \n     \n     \n███  \n███  \n███  \n     \n     \n     \n███  \n███  \n███  \n     \n     \n     \n',
        'a' : '      \n      \n      \n      \n      \n      \n      \n      \n      \n      \n ██   \n█ █   \n█ █   \n ███  \n           \n',
        'm' : '       \n       \n       \n       \n       \n       \n       \n       \n       \n       \n       \n█████  \n█ █ █  \n█ █ █  \n       \n',
        'p' : '     \n     \n     \n     \n     \n     \n     \n     \n     \n     \n     \n███  \n█ █  \n███  \n█    \n',
        ' ' : '     \n     \n     \n     \n     \n     \n     \n     \n     \n     \n     \n     \n     \n     \n     \n',
    }

    def __init__(self, parser = None):
        """
        The constructor of this class.
        """
        ScreenBase.__init__(self,
            "clock",
            _("displays a digital clock on screen"),
            parser
        )
        if self.parser:
            self.parser.add_argument("-m","--ampm", help="Use a 12 hour clock with am/pm suffix.", action="store_true", default=False)
            self.parser.add_argument("-b","--big", help="Big mode using a constrast block method.", action="store_true", default=False)

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

        print(text)

        sleep_time = 1 # usually one cycle per second
        if self.ampm:
            # special case to show blinking separator
            sleep_time = 0.7

        time.sleep(sleep_time)

    def _usage_options_example(self):
        return (_("""
        termsaver clock -mb         Shows the clock in 12 hour and big mode.
        termsaver clock --big       Shows the clock in big mode."""))

    def _parse_args(self, launchScreenImmediately=True):
        
        args, unknown = self.parser.parse_known_args()

        self.ampm = args.ampm
        self.big = args.big
        
        if (self.big):
            self.lineindigimap = 15
            self.digmap = self.digimapbig

        if launchScreenImmediately:
            self.autorun()
        else:
            return self
            

    def get_ascii_time(self, date_time):
        """
        Returns the ASCII representation of a date.
        """

        # shows/hides separator for a blinking effect
        # Moved here so as not to duplicate in big number. Default used self.cseparator
        separator = ""
        if self.show_separator:
            separator = self.cseparator
            self.show_separator = False
        else:
            separator = " "
            self.show_separator = True

        # define clock string based on options (12/24)
        if self.ampm:
            hour = int(date_time.strftime('%H'))

            suffix = "am"
            if hour >= 12:
                suffix = "pm"

            # fix the hour value into modulus of 12
            hour = hour % 12
            # fix the zero hour value
            if hour == 0:
                hour = 12
            clock = "%s%s%s%s" % (hour, separator, date_time.strftime('%M'), suffix)
        elif self.big:
            clock = date_time.strftime('%H' + separator + '%M')
        else:
            # 24hs format includes seconds
            clock = date_time.strftime('%H' + self.cseparator + '%M' + self.cseparator + '%S')

        items = []
        for c in clock:
            items.append(self.digmap[c])
        output = ''
        for i in range(self.lineindigimap):  # loop lines of chars - Increased to six for extra font line
            temp = ''
            for item in items:
                temp += item.split('\n')[i]
            output += temp + '\n'

        return output
