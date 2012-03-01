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

    * `Jokes4AllRSSFeedScreen`
"""

#
# Internal modules
#
from termsaverlib.screen.base.rssfeed import SimpleRSSFeedScreenBase
from termsaverlib.i18n import _


class Jokes4AllRSSFeedScreen(SimpleRSSFeedScreenBase):
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

    def __init__(self):
        """
        The constructor of this class, using most default values from its super
        class, `SimpleRSSFeedScreenBase`.

        NOTE: Maybe NSFW (Not Safe For Work)
        """
        SimpleRSSFeedScreenBase.__init__(self,
            "jokes4all",
            _("displays recent jokes from jokes4all.net (NSFW)"),
            "http://jokes4all.net/rss/360010113/jokes.xml",
            ["pubDate", "link", "description"],
            '\n%(description)s\n\n%(pubDate)s %(link)s\n',
            0.015
        )

        # set defaults for this screen
        self.sleep_between_items = 30
        self.line_delay = 0
        self.cleanup_per_item = True
        self.cleanup_per_cycle = True
        self.center_vertically = True
