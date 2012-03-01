###############################################################################
#
# file:     rssfeed.py
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
Simple screensaver that displays data from a RSS feed.

See additional information in the class itself.

The screen class available here is:

    * `RSSFeedScreen`
"""

#
# Internal modules
#
from termsaverlib.screen.base.rssfeed import RSSFeedScreenBase
from termsaverlib import constants
from termsaverlib.i18n import _


class RSSFeedScreen(RSSFeedScreenBase):
    """
    Simple screensaver that displays data from a RSS feed.

    RSS Feed Screen configuration:

      * sleep between items: 3 seconds

      * clean up each cycle: True
        this will force the screen to be cleaned (cleared) before each joke
        is displayed

      * character display delay: 0.015
        a bit faster than traditional speeds, because users are not
        interested in the char print animation as much.

      * clean up each item: False

      * display format:

          '%(title)s (%(pubDate)s)\n%(description)s\n%(link)s\n.\n'
    """

    def __init__(self):
        """
        Creates a new instance of this class.
        """
        RSSFeedScreenBase.__init__(self,
            "rssfeed",
            _("displays rss feed information"),
            None,
            ["pubDate", "title", "link", "description"],
            '%(title)s (%(pubDate)s)\n%(description)s\n%(link)s\n.\n',
        )

        # set defaults for this screen
        self.cleanup_per_cycle = True
        self.cleanup_per_item = False
        self.sleep_between_items = 3
        self.delay = 0.015

    def _message_no_url(self):
        """
        Defines a method to be overriden by inheriting classes, with the
        purpose to display extra help information for specific errors.
        """
        return _("""
You just need to provide the URL of the RSS feed from where %(app_title)s will
read and display on screen.

If you do not have any idea which RSS to use, check out some examples here:

    CNN
        Top Stories - http://rss.cnn.com/rss/edition.rss
        World       - http://rss.cnn.com/rss/edition_world.rss
        Technology  - http://rss.cnn.com/rss/edition_technology.rss

        See CNN's complete list of RSS syndication here:
            http://edition.cnn.com/services/rss/

    Lifehacker - http://www.lifehacker.com/index.xml
    Note: Lifehacker uses HTML to deliver "description" contents in the RSS,
          so you might need to change the format to something like:
               --format "%%(title)s (%%(pubDate)s)\\n"
""") % {
       'app_title': constants.App.TITLE,
    }
