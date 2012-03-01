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

    * `AsciArtFartsScreen`
"""

#
# Internal modules
#
from termsaverlib.screen.base.rssfeed import SimpleRSSFeedScreenBase
from termsaverlib.i18n import _


class AsciArtFartsScreen(SimpleRSSFeedScreenBase):
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

    def __init__(self):
        """
        The constructor of this class, using most default values from its super
        class, `SimpleRSSFeedScreenBase`.

        The display of the ascii arts here are basically based on getting the
        description tag of the RSS feed, that constains a dirty HTML ascii art.

        NOTE: Maybe NSFW (Not Safe For Work)
        """
        super(AsciArtFartsScreen, self).__init__(
            "asciiartfarts",
            _("displays ascii images from asciiartfarts.com (NSFW)"),
            'http://www.asciiartfarts.com/farts.rss',
            ["description"],
            "%(description)s",
        )

        # set defaults for this screen
        self.cleanup_per_cycle = True
        self.sleep_between_items = 5
        self.center_vertically = True
        self.center_horizontally = True
        self.clean_dirt = ['<pre>', '</pre>']
        self.cleanup_per_item = True
