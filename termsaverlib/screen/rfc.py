###############################################################################
#
# file:     rfc.py
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
A simple screen that fetches documents from RFC (Request for Comments).

The screen class available here is:

    * `RFCScreen`
"""

#
# Python built-in modules
#
import random

#
# Internal modules
#
from termsaverlib.screen.base.urlfetcher import SimpleUrlFetcherBase
from termsaverlib.i18n import _


class RFCScreen(SimpleUrlFetcherBase):
    """
    A simple screen that fetches documents from RFC (Request for Comments).

    Request for Comments (RFC) is a memorandum published by the Internet
    Engineering Task Force (IETF) describing methods, behaviors, research, or
    innovations applicable to the working of the Internet and Internet-
    connected systems.

    More information about RFC at Wikipedia:
    http://en.wikipedia.org/wiki/Request_for_Comments

    This screen basically does the same as its super class,
    `SimpleUrlFetcherBase`, with a simple difference that it must randomize
    the URL to be fetched in every screen cycle. This is done by overriding
    the `run` command.

    The list of valid RFCs, according to Wikipedia, are listed in `valid_rfc`.
    Although this may vary in time, small out-of-date information will still
    not affect the main purpose of this screen.
    """

    valid_rfc = [
         768, 791, 792, 793, 826, 854, 855, 862, 863, 864, 868, 903,
        1034, 1035, 1036, 1058, 1059, 1087, 1112, 1119, 1149, 1157, 1176, 1294,
        1305, 1321, 1350, 1436, 1441, 1459, 1730, 1777, 1855, 1889, 1918, 1939,
        1945, 1948, 1950, 1951, 1952, 1964, 1991, 2080, 2119, 2131, 2177, 2195,
        2228, 2246, 2251, 2252, 2253, 2254, 2255, 2256, 2326, 2327, 2328, 2351,
        2362, 2397, 2407, 2408, 2409, 2440, 2445, 2453, 2460, 2549, 2570, 2606,
        2616, 2740, 2743, 2744, 2810, 2811, 2812, 2813, 2821, 2822, 2853, 2865,
        2866, 2965, 2974, 3022, 3031, 3056, 3080, 3162, 3261, 3284, 3286, 3315,
        3339, 3376, 3401, 3402, 3403, 3404, 3405, 3501, 3530, 3720, 3783, 3801,
        3977, 4213, 4217, 4271, 4287, 4251, 4291, 4353, 4408, 4422, 4541, 4575,
        4579, 4634, 4646, 4787, 4960, 5023, 5533, 5969, 6455, 937, 951, 959,
    ]
    """
    Extracted from Wikipedia: http://en.wikipedia.org/wiki/List_of_RFCs
    on 2012-02-28, 02:11 AM
    """

    url_format = "http://tools.ietf.org/rfc/rfc%d.txt"
    """
    The URL format that can return a text version of a specific RFC number.
    """

    def __init__(self):
        """
        The constructor of this class, using most default values from its super
        class, `SimpleUrlFetcherBase`.
        """
        SimpleUrlFetcherBase.__init__(self,
            "rfc",
            _("randomly displays RFC contents"),
            "localhost")  # base class require a URL

    def _run_cycle(self):
        """
        Executes a cycle of this screen. Overriden from its superclass because
        it needs to must randomize the URL to be fetched in every screen cycle.
        """
        # Randomize next URL to fetch from one of the valid list
        self.url = self.url_format % self.valid_rfc[
            random.randint(0, len(self.valid_rfc) - 1)]

        data = self.fetch(self.url)
        self.clear_screen()
        self.typing_print(data)
