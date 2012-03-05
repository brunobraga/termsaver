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
A helper class used for screens that require Internet connectivity. See
additional information in the class itself.

The helper class available here is:

    * `URLFetcherHelperBase`

"""

#
# Python built-in modules
#
from urllib2 import Request, urlopen, URLError, HTTPError
import urlparse
import time

#
# Internal modules
#
from termsaverlib.screen.helper import ScreenHelperBase
from termsaverlib import exception, constants
from termsaverlib.i18n import _


class URLFetcherHelperBase(ScreenHelperBase):
    """
    A helper class that provides Internet connectivity for termsaver screens.
    The functionalities available are:

        * fetch data over the Internet (only text-base)
        * avoid too many requests at a time (configured at
          `constants.Settings.FETCH_INTERVAL_SECONDS`

    For these functionalities, the following methods are publicly available:

        * `fetch`: for a specified URI, it returns its string contents
           additionally, this will also set a `raw` property with the data
           last fetched.

        * `fix_uri`: uses an algorithm to fix and validate a string as URL
          format. This should be used to prepare the URL before calling `fetch`
          method.

    """

    __last_fetched = None
    """
    A flag that defines the EPOCH time when the last fetch occurred, to ensure
    termsaver application does not keep connecting to the Internet without need

    See also: `constants.Settings.FETCH_INTERVAL_SECONDS`
    """

    raw = ""
    """
    The raw text data that is fetched using urllib. This can be later
    manipulated as needed (xml parsing, etc).
    """

    def fix_uri(self, text):
        """
        Validates a text as URL format, also adjusting necessary stuff for a
        clearer URL that will be fetched here.

        Code based on Django source:
        https://code.djangoproject.com/browser/django/trunk/django/forms/
        fields.py?rev=17430#L610

        Arguments:

            * text: the URL string that is to be validated and fixed
        """
        if not text:
            raise exception.UrlException(text, _("URL can not be blank"))
        try:
            url_fields = list(urlparse.urlsplit(text))
        except ValueError:
            raise exception.UrlException(text, _("URL does not seem valid"))

        if not url_fields[0]:
            # If no URL scheme given, assume http://
            url_fields[0] = 'http'
        if not url_fields[1]:
            # Assume that if no domain is provided, that the path segment
            # contains the domain.
            url_fields[1] = url_fields[2]
            url_fields[2] = ''
            # Rebuild the url_fields list, since the domain segment may now
            # contain the path too.
            try:
                url_fields = list(urlparse.urlsplit(
                    urlparse.urlunsplit(url_fields)))
            except ValueError:
                raise exception.UrlException(text,
                    _("URL does not seem valid"))

        if not url_fields[2]:
            # the path portion may need to be added before query params
            url_fields[2] = '/'
        return urlparse.urlunsplit(url_fields)

    def fetch(self, uri):
        """
        Executes the fetch action toward a specified URI. This will also
        try to avoid unnecessary calls to the Internet by setting the flag
        `__last_fetched`. If it can not fetch again, it will simply return
        the `raw` data that was previously created by a previous fetch.

        Arguments:

            * uri: the path to be fetched
        """
        # check if we can fetch again
        if self.__last_fetched and not self.raw and \
                time.time() - self.__last_fetched < \
                constants.Settings.FETCH_INTERVAL_SECONDS:
            return self.raw

        headers = {'User-Agent': "%s/%s" % (constants.App.NAME,
                                            constants.App.VERSION)}
        # separate possible querystring data from plain URL
        temp = uri.split('?')
        url = temp[0]
        if len(temp) > 1:  # old style condition for old python compatibility
            data = temp[1]
        else:
            data = None

        self.log(_("Connecting to %s ... (this could take a while)") % uri)

        # execute URL fetch
        req = Request(url, data, headers)
        resp = None
        try:
            resp = urlopen(req)
        except HTTPError, e:
            raise exception.UrlException(uri,
                _("Fetched URL returned error %d.") % e.code)
        except URLError, e:
            raise exception.UrlException(uri,
                _("Could not fetch URL, because %s") % e.reason)
        else:
            self.__last_fetched = time.time()

            self.raw = resp.read()

            # make sure the content is not binary (eg. image)
            if self.__is_response_binary(self.raw):
                raise exception.UrlException(uri, _("Fetched data is binary."))
        finally:
            if resp:
                resp.close()

        return self.raw

    def __is_response_binary(self, raw):
        """
        Returns True if the given data is binary in nature, and False otherwise

        For the merit of being a binary file (i.e., termsaver will not be able
        to handle it), it is safe enough to consider the above True, as any
        files in this situation will be simply skipped, avoiding weird errors
        being thrown to the end-user.

        Arguments:

            raw: the response data that must be tested for binary values
        """
        return raw.find("\0") > -1
