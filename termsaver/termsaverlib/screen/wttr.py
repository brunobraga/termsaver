###############################################################################
#
# file:     wttr.py
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
Simple screensaver that displays data from wttr.in.
"""

import sys
import time

#
# Internal modules
#
from termsaver.termsaverlib import constants
from termsaver.termsaverlib.i18n import _
from termsaver.termsaverlib.screen.base import ScreenBase
from termsaver.termsaverlib.screen.base.urlfetcher import SimpleUrlFetcherBase
from termsaver.termsaverlib.screen.helper.position import PositionHelperBase


class WTTRScreen(SimpleUrlFetcherBase, PositionHelperBase):
    
    units = None
    typing = False
    narrow = False
    
    def __init__(self, parser = None):

        SimpleUrlFetcherBase.__init__(self,
            "wttr",
            _("displays a weather report from wttr.in"),
            parser,
            'https://wttr.in/?a'
        )

        # # set defaults for this screen
        # self.cleanup_per_cycle = True
        # self.cleanup_per_item = False
        self.sleep_between_items = 20
        # self.delay = 0.015

        if self.parser:
            self.parser.add_argument("-d", "--delay", help="Delay in seconds between weather refresh. Lower this when using --typing mode.", type=int, default=300) # 5 minutes
            # self.parser.add_argument("-l", "--location", help="Location to fetch weather for", type=str, default="")
            self.parser.add_argument("-t", "--typing", help="Types the weather report out instead of printing it", action="store_true", default=False)
            self.parser.add_argument("-u", "--units", help="Units to use for temperature and wind speed.", type=str, default=None, choices=["metric", "imperial"])
            self.parser.add_argument("-n", "--narrow", help="Narrow the output to 80 characters", action="store_true", default=False)

    def _run_cycle(self):

        self.clear_screen()
        
        additions = ""
        if self.units is not None:
            additions += "m" if self.units == "metric" else "u"
        if self.narrow:
            additions += "n"
        if additions != "":
            self.url += additions
        new_text = self.fetch(self.url, 'GET', 'curl/7.37.0',).decode("utf-8")
        self.get_terminal_size()
        new_text = self.center_text_vertically(new_text)
        # This breaks the layout it but I'm not exactly sure why.
        #new_text = self.center_text_horizontally(new_text)
        if self.typing_print:
            self.typing_print(new_text)
        else:
            print(new_text)
        time.sleep(self.sleep_between_items)

    def _parse_args(self, launchScreenImmediately=True):
        args, unknown = self.parser.parse_known_args()
        self.sleep_between_items = args.delay
        self.typing = args.typing
        self.units = args.units
        self.narrow = args.narrow
        # self.location = args.location
        if launchScreenImmediately:
            self.autorun()
        else:
            return self