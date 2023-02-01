###############################################################################
#
# file:     jokes4all.py
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
Simple screensaver that displays recent jokes from http://jokes4all.net
website, from its hourly updated RSS feed.

See additional information in the class itself.

The screen class available here is:

    * `Jokes4AllScreen`
"""

import time

from termsaver.termsaverlib.i18n import _
from termsaver.termsaverlib.screen.base import ScreenBase
#
# Internal modules
#
from termsaver.termsaverlib.screen.base.urlfetcher import SimpleUrlFetcherBase
from termsaver.termsaverlib.screen.helper.position import PositionHelperBase


class Jokes4AllRSSFeedScreen(SimpleUrlFetcherBase, PositionHelperBase):
    """
    Simple screensaver that displays recent jokes from http://jokes4all.net
    website, from its hourly updated RSS feed.

    RSS Feed Screen configuration:

      * sleep between items: 30 seconds
        this is to allow people enough time for them to read the joke

      * clean up each cycle: True
        this will force the screen to be cleaned (cleared) before each joke
        is displayed

      * character display delay: 0.015
        a bit faster than traditional speeds, because users are not
        interested in the char print animation as much.

      * clean up each item: True
        this will force the screen to be cleaned (cleared) before each image
        is displayed

      * display format:

          '\n%(description)s\n\n%(pubDate)s %(link)s\n'

      * center in vertical
    """

    def __init__(self, parser = None):
        """
        The constructor of this class, using most default values from its super
        class, `SimpleRSSFeedScreenBase`.

        NOTE: Maybe NSFW (Not Safe For Work)
        """
        SimpleUrlFetcherBase.__init__(self,
          'jokes4all',
          _("displays random jokes from jokes4all.net (NSFW)"),
          parser,
          'https://jokes4all.net'
        )
        

        # set defaults for this screen
        self.sleep_between_items = 30
        self.line_delay = 0
        self.cleanup_per_item = True
        self.cleanup_per_cycle = True
        self.center_vertically = True
        
        if self.parser:
          self.parser.add_argument("-d", "--delay", help="Delay in seconds between jokes", type=int, default=self.sleep_between_items)

    def _parse_args(self, launchScreenImmediately=True):
      args, unknown = self.parser.parse_known_args()

      if args.delay:
        self.sleep_between_items = args.delay
      
      if launchScreenImmediately:
        self.autorun()
      else:
        return self

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

    def process_data(self, data):
      data_string = data.decode('utf-8')
      # Get the text between the first <div class='joke'> and the next </div>
      data_string = data_string.split('<div class="joke">')[1].split('</div>')[0]
      if (data_string):
        data_string = data_string.replace("<br>", "\n")
      # data_string = data_string.split('<pre>')[2].split('</pre>')[0]
      return data_string.encode('utf-8')