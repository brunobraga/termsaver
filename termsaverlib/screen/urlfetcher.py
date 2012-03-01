###############################################################################
#
# file:     urlfetcher.py
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
Simple screensaver that displays data from a URL.

See additional information in the class itself.

The screen class available here is:

    * `UrlFetcherScreen`
"""

#
# Internal modules
#
from termsaverlib.screen.base.urlfetcher import UrlFetcherBase
from termsaverlib import constants
from termsaverlib.i18n import _


class UrlFetcherScreen(UrlFetcherBase):
    """
    Simple screensaver that displays data from a URL.
    """

    def __init__(self):
        """
        Creates a new instance of this class.
        """
        UrlFetcherBase.__init__(self,
            "urlfetcher",
            _("displays url contents with typing animation"))

    def _message_no_url(self):
        """
        """
        return _("""
You just need to provide the URL from where %(app_title)s will read and
display on screen.

If you do not have any idea which URL to use, check out some examples here:

    RFC
        RFC-1034 - http://tools.ietf.org/rfc/rfc1034.txt

        See a RFC list from Wikipedia:
            http://en.wikipedia.org/wiki/List_of_RFCs
        (remember to use the txt version)

""") % {
       'app_title': constants.App.TITLE,
    }
