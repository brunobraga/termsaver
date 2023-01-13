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
This module contains a screen base class that handles RSS feeds display.
See additional information in the class itself.

The helper classes available here are:

    * `RSSFeedScreenBase`
    * `SimpleRSSFeedScreenBase`
"""

#
# Python built-in modules
#
import time

from termsaver.termsaverlib import common, constants, exception
from termsaver.termsaverlib.i18n import _
#
# Internal modules
#
from termsaver.termsaverlib.screen.base import ScreenBase
from termsaver.termsaverlib.screen.base.urlfetcher import UrlFetcherBase
from termsaver.termsaverlib.screen.helper.position import PositionHelperBase
from termsaver.termsaverlib.screen.helper.typing import TypingHelperBase
from termsaver.termsaverlib.screen.helper.xmlreader import XMLReaderHelperBase


class RSSFeedScreenBase(UrlFetcherBase,
                        TypingHelperBase,
                        PositionHelperBase,
                        XMLReaderHelperBase):
    """
    A base class used to handle RSS feeds, and display them accordingly.
    This also includes the `TypingHelperBase` and `PositionHelperBase` to
    add functionality of typing writer display, and certain positioning
    features.

    The instantiation of this class takes two additional arguments, compared
    with its base class:

        * tags: defines the list of string tags of the RSS that you are
          interest in. Accepted values are:
               * pubDate
               * title
               * link
               * description

        * print_format: defines the formating to be printed out, based on
          the tags available (use python string format with dictionary. eg.
          '%(title)s (%(pubDate)s)\n\n')

    When inheriting from this screen, you can also take advantage of the
    following properties and functionalities:

        * `sleep_between_items`: Sleeping time, in seconds, between each RSS
           item displayed.

        * `cleanup_per_item`: Defines if termsaver should clean the screen for
           each item being read

        * `center_vertically`: Defines if the information displayed should be
           vertically centered on screen.

        * `center_horizontally`: Defines if the information displayed should be
           horizontally centered on screen.
    """

    sleep_between_items = 1
    """
    Sleeping time, in seconds, between each RSS item displayed.
    """

    cleanup_per_item = False
    """
    Defines if termsaver should clean the screen for each item being read
    """

    center_vertically = False
    """
    Defines if the information displayed should be vertically centered on
    screen.
    """

    center_horizontally = False
    """
    Defines if the information displayed should be horizontally centered on
    screen.
    """

    clean_html = True
    """
    Defines that the output text must be cleaned from HTML tags.
    """

    def __init__(self, parser, url=None,
                  tags=None, print_format=None, delay=None):
        """
       Creates a new instance of this class.

        This constructor has two additional arguments, compared with its base
        class:

            * tags: defines the list of string tags of the RSS that you are
              interest in. Accepted values are:
                   * pubDate
                   * title
                   * link
                   * description

            * print_format: defines the formating to be printed out, based on
              the tags available (use python string format with dictionary. eg.
              '%(title)s (%(pubDate)s)\n\n')
        """

        UrlFetcherBase.__init__(self, parser, url, delay)
        XMLReaderHelperBase.__init__(self, "item", tags)
        
        if self.parser != None:
            self.parser.add_argument("-u", "--url", help="The rss feed url", type=str)
            self.parser.add_argument("-r", "--raw", help="Shows all text available (with HTML if any)", action="store_true")
            
            #if not hasFormat:
            self.parser.add_argument("-f", "--format",type=str, action="store", help="""|R
            The printing format according to values available in RSS feed:
                    * pubDate
                    * title
                    * link
                    * description
            You must use python dictionary based formatting style
            (see examples for details)""")
        
        self.print_format = print_format
        if not print_format:
            self.print_format = '%(title)s (%(pubDate)s)\n\n'

    def _parse_args(self, launchScreenImmediately=True):
        """
        Handles the special command-line arguments available for this screen.
        Although this is a base screen, having these options prepared here
        can save coding for screens that will not change the default options.

        See `_usage_options_example` method for documentation on each of the
        options being parsed here.

        Additionally, this is dependent on the values exposed in `cli_opts`,
        passed to this class during its instantiation. Only values properly
        configured there will be accepted here.
        """
        args, unknown = self.parser.parse_known_args()
        
        if args.raw:
            self.clean_html = False

        if args.format:
            self.print_format = common.unescape_string(args.format)

        if args.url:
            try:
                # try to fix the url formatting
                self.url = self.fix_uri(args.url)
            except Exception as e:
                error_message = ""
                if hasattr(e, 'message'):
                    error_message = e.message
                else:
                    error_message = e
                raise exception.InvalidOptionException("url", error_message)
        else:
            raise exception.InvalidOptionException("url", "URL is required")
        
        if launchScreenImmediately:
            self.autorun()
        else:
            return self

    def _run_cycle(self):
        """
        Executes a cycle of this screen.

        The actions taken here, for each cycle, are as follows:

            * retrieve data from `url`
            * parses the data into a XML dom document object
            * parses the document object into a list of dictionaries
            * print using `typing_print`
        """
        self.doc_xml_string(self.fetch(self.url))
        self.parse_data()
        self.clear_screen()

        for item in self.data:
            new_text = item
            try:
                new_text = common.unescape_string(self.print_format % new_text)
                # remove HTML tags is applicable
                if self.clean_html:
                    new_text = common.strip_html(new_text)
            except:
                raise exception.InvalidOptionException("format",
                    _("There was an error while using your format."))

            if self.center_vertically or self.center_horizontally:
                self.get_terminal_size()

                if self.center_vertically:
                    new_text = self.center_text_vertically(new_text)
                if self.center_horizontally:
                    new_text = self.center_text_horizontally(new_text)

            self.typing_print(new_text)
            time.sleep(self.sleep_between_items)

            if self.cleanup_per_item:
                self.clear_screen()


class SimpleRSSFeedScreenBase(ScreenBase, RSSFeedScreenBase):
    """
    Inherits the `RSSFeedScreenBase` class to handle basic RSS parsing.
    This will simplify the use of RSSFeedScreenBase by forcing a fixed
    URL feed, and simplify the code of screens inheriting from it.
    """

    def __init__(self, name, description, parser, url, 
                 tags=None, print_format=None, delay=None):
        """
        Creates a new instance of this class.

        This constructor has forced the url argument, compared with its base
        class, as it has no command line options to define its value manually
        """
        ScreenBase.__init__(self, name, description, parser)
        RSSFeedScreenBase.__init__(self,
                parser, url, tags,
                print_format, delay
        )
    
    def _run_cycle(self):
        RSSFeedScreenBase._run_cycle(self)
