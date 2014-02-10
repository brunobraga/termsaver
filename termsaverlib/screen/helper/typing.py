###############################################################################
#
# file:     typing.py
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
A helper class used for screens that require more dynamic output to users.
See additional information in the class itself.

The helper class available here is:

    * `TypingHelperBase`

"""
#
# Python built-in modules
#
import sys
import time

#
# Internal modules
#
from termsaverlib.screen.helper import ScreenHelperBase
from termsaverlib import constants


class TypingHelperBase(ScreenHelperBase):
    """
    This helper class gives functionality to screens to print out information
    in a more interactive way, simulating a typing writer machine, based on
    two main speed control properties:

        * `delay`: defines the delay for printing out characters of a string

        * `line_delay`: defines the delay for printing out new lines within a
          string (sometimes, setting different proportions make a lot of a
          difference)

    If no values are defined by the screen itself, default values should be
    used. The `delay` is set in `constants.Settings.CHAR_DELAY_SECONDS`, and
    the `line_delay` is 10 times the value of delay.

    To use this screen helper is pretty straightforward, just call the method:

        * `typing_print`: this will print the specified text string using the
           speed controls `delay` and `line_delay`.

    """

    delay = None
    """
    Defines the character printing delay, to give a cool visual of a
    typing machine. This value is measured in seconds, and default marks are
    defined in `constants.Settings.CHAR_DELAY_SECONDS`.
    """

    line_delay = None
    """
    Defines the delay imposed to every new line prior to char printing. By
    default, its value is 10x the `delay`.
    """

    def typing_print(self, text):
        """
        Prints text with standard output to allow side-by-side printing, and
        give the impression of a typing writer machine. The speed is controlled
        by properties of this class: `delay` and `line_delay`.

        Arguments:

            * text: the text to be printed in typing style

        Notes:

            * This also supports new lines (\n)
            * blank spaces, due to its lack of meaning, are ignored for speed
              limiting, so they will be flushed all at once.

        """
        # set defaults
        if self.delay is None:
            self.delay = constants.Settings.CHAR_DELAY_SECONDS

        if self.line_delay is None:
            self.line_delay = 10 * self.delay
        splitText = text.split('\n')
        for line in splitText:
            for char in line:
                sys.stdout.write(char)

                # only pause if it is not a blank space
                if char != ' ':
                    time.sleep(self.delay)

                sys.stdout.flush()

            # need to re-print the line removed from the split
            sys.stdout.write('\n')

            time.sleep(self.line_delay)  # specific pause for new lines
