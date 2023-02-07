###############################################################################
#
# file:     starwars.py
#
# Purpose:  An attempt at the starwars asciimation
#
# Note:     This file is part of Termsaver application, and should not be used
#           or executed separately.
#
###############################################################################
#
# Copyright 2020 Termsaver
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
This module contains a simple screen that loads the sw1.txt file used by
the star wars asciimation.

The screen class available here is:

    * `StarWarsScreen`
"""

import io
import itertools
import time
from pathlib import Path

from termsaver.termsaverlib import common
from termsaver.termsaverlib.i18n import _
#
# Internal modules
#
from termsaver.termsaverlib.screen.base import ScreenBase
from termsaver.termsaverlib.screen.helper.position import PositionHelperBase


class StarWarsScreen(ScreenBase, PositionHelperBase):
    """
    Screen that displays the star wars text from the
    star wars asciimation.
    (http://www.asciimation.co.nz/).

    From its base classes, the functionality provided here bases on the
    settings defined below:

        * clean up each cycle: True
          this will force the screen to be cleaned (cleared) before each new
          cycle is displayed
    """

    def __init__(self, parser = None):
        """
        The constructor of this class.
        """
        ScreenBase.__init__(self,
            "starwars",
            _("displays the star wars asciimation on screen"),
            parser
        )
        self.cleanup_per_cycle = True
        self.is_initalized = False

    def reshape(self,lst, n):
        return [lst[i*n:(i+1)*n] for i in range(len(lst)//n)]

    def _run_cycle(self):
        """
        Executes a cycle of this screen.
        """
        
        if self.is_initalized is False:
            filepath = Path(__file__).resolve().parent.parent.parent / "data" / "sw1.txt"
            with io.open(filepath,"rb") as swfile:
                lines = swfile.readlines()
                lines = [line.decode('utf-8') for line in lines]

                self.current_frame = 0
                self.star_wars = self.reshape(lines,14)
                self.time_per_frame = 15
                self.is_initalized = True

        frame_time = float(self.star_wars[self.current_frame][0]) / self.time_per_frame
        print("\r\n" + "".join(self.star_wars[self.current_frame][1:14]))
        time.sleep(frame_time)
        self.current_frame += 1

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

    The Star Wars Asciimation is copyright Simon Jansen (jansens@asciimation.co.nz)
    and viewable standalone on the web at http://asciimation.co.nz.

    Options:
    -h, --help   Displays this help message
        
    """))

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

        if launchScreenImmediately:
            self.autorun()
        else:
            return self
