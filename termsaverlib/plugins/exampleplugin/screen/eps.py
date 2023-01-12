###############################################################################
#
# file:     ExamplePluginScreen.py
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
This module contains an example plugin screen.

The screen class available here is:

    * `ExamplePluginScreen`
"""

#
# Internal modules
#
from termsaverlib.screen.base import ScreenBase
from termsaverlib.screen.helper.position import PositionHelperBase
from termsaverlib import common
from termsaverlib.i18n import _, set_app

import itertools

import time
import io

from termsaverlib.plugins.exampleplugin.screen.base import ExamplePluginScreenBase

set_app("termsaver-exampleplugin")

class ExamplePluginScreen(ExamplePluginScreenBase):
    """
    An Example Plugin Screen
    """

    def __init__(self, parser = None):
        """
        The constructor of this class.
        """
        ScreenBase.__init__(self,
            "exampleplugin",
            _("the example plugin"),
            parser
        )
        self.cleanup_per_cycle = True

    def _run_cycle(self):
        """
        Executes a cycle of this screen.
        """
        
        print(self.example_echo("Hello World"))
        time.sleep(1)

    def _parse_args(self, launchScreenImmediately=True):
        """
        Handles the special command-line arguments available for this screen.
        Although this is a base screen, having these options prepared here
        can save coding for screens that will not change the default options.

        Additionally, this is dependent on the values exposed in `cli_opts`,
        passed to this class during its instantiation. Only values properly
        configured there will be accepted here.
        """

        # This will parse out all known and unknown arguments.
        # See the documentation on the argparse library.
        args, unknown_args = self.parser.parse_known_args()
        
        if launchScreenImmediately:
            self.autorun()
        else:
            return self
