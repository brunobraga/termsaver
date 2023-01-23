###############################################################################
#
# file:     asciiartfarts.py
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
This module contains a simple screen that connects to asciiartfarts.com RSS
feeds to display ascii arts on screen.
See additional information in the class itself.

The screen class available here is:

    * `AsciiArtFartsScreen`
"""

import time

from termsaver.termsaverlib.i18n import _
#
# Internal modules
#
from termsaver.termsaverlib.screen.base.urlfetcher import SimpleUrlFetcherBase
from termsaver.termsaverlib.screen.helper.position import PositionHelperBase


class AsciiArtFartsScreen(SimpleUrlFetcherBase, PositionHelperBase):
    """
    A simple screen that connects to asciiartfarts.com RSS feeds to display
    ascii arts on screen.

    From its base classes, the functionality provided here bases on the
    settings defined below:

        * sleep between items: 5 seconds
          not so much time between images

        * clean up each cycle: True
          this will force the screen to be cleaned (cleared) before each new
          cycle is displayed

        * center in vertical

        * center in horizontal

        * clean dirt: HTML <pre> tags

        * clean up each item: True
          this will force the screen to be cleaned (cleared) before each image
          is displayed
    """

    def __init__(self, parser = None):
        """
        The constructor of this class, using most default values from its super
        class, `SimpleRSSFeedScreenBase`.

        The display of the ascii arts here are basically based on getting the
        description tag of the RSS feed, that constains a dirty HTML ascii art.

        NOTE: Maybe NSFW (Not Safe For Work)
        """
        SimpleUrlFetcherBase.__init__(self,
            "asciiartfarts",
            _("displays ascii images from asciiartfarts.com (NSFW)"),
            parser,
            'http://www.asciiartfarts.com/random.cgi',
        )

        if self.parser:
          self.parser.add_argument("-d", "--delay", help="Delay in seconds between images", type=int, default=5)

    def _run_cycle(self):
        """
        Executes a cycle of this screen. Overriden from its superclass because
        it needs to must randomize the URL to be fetched in every screen cycle.
        """
        self.clear_screen()
        new_text = self.process_data(self.fetch(self.url)).decode("utf-8")
        self.get_terminal_size()
        new_text = self.center_text_vertically(new_text)
        new_text = self.center_text_horizontally(new_text)
        self.typing_print(new_text)
        time.sleep(self.sleep_between_items)

    def _parse_args(self, launchScreenImmediately=True):
      args, unknown = self.parser.parse_known_args()
      self.sleep_between_items = args.delay
      if launchScreenImmediately:
        self.autorun()
      else:
        return self

    def process_data(self, data):
      data_string = data.decode('utf-8')
      data_string = data_string.split('<pre>')[2].split('</pre>')[0]
      return data_string.encode('utf-8')