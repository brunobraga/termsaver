###############################################################################
#
# file:     SamplePluginScreen.py
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

    def __init__(self):
        """
        The constructor of this class.
        """
        ScreenBase.__init__(self,
            "exampleplugin",
            _("the example plugin"),
            {'opts': 'h', 'long_opts': ['help']})
        self.cleanup_per_cycle = True

    def _run_cycle(self):
        """
        Executes a cycle of this screen.
        """
        
        print(self.example_echo("Hello World"))
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
            print (_("""

            This is the example plugin. There are no options!

            Options:
            -h, --help   Displays this help message
        
    """))

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
            else:
                # this should never happen!
                raise Exception(_("Unhandled option. See --help for details."))
