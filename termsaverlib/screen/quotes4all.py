###############################################################################
#
# file:     quotes4all.py
#
# Purpose:  holds base classes used by screens in termsaver
#           refer to module documentation for details
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

    * `Quotes4AllRSSFeedScreen`
"""

#
# Internal modules
#
from termsaverlib.screen.base.rssfeed import SimpleRSSFeedScreenBase
from termsaverlib.i18n import _


class Quotes4AllRSSFeedScreen(SimpleRSSFeedScreenBase):
    """
    Simple screensaver that displays recent jokes from http://jokes4all.net
    website, from its hourly updated RSS feed.

    RSS Feed Screen configuration:

        * sleep between items: 10 seconds
          this is to allow people enough time for them to read the quote

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

          '\n"%(description)s" -- %(title)s\n'

        * center in vertical

        * center in horizontal

        * clean dirt: new lines

    """

    def __init__(self):
        """
        Creates a new instance of this class (used by termsaver script)
        """
        SimpleRSSFeedScreenBase.__init__(self,
            "quotes4all",
            _("displays recent quotes from quotes4all.net"),
            "http://quotes4all.net/rss/360010110/quotes.xml",
            ["title", "description"],
            '"%(description)s" -- %(title)s',
            0.015
        )

        # set defaults for this screen
        self.sleep_between_items = 10
        self.line_delay = 0
        self.cleanup_per_cycle = True
        self.cleanup_per_item = True
        self.center_vertically = True
        self.center_horizontally = True
        self.clean_dirt = ["\n", "  "]
