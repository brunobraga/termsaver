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

#
# Internal modules
#
from termsaverlib.screen.base.urlfetcher import UrlFetcherBase
from termsaverlib.screen.helper.xmlreader import XMLReaderHelperBase
from termsaverlib.screen.helper.typing import TypingHelperBase
from termsaverlib.screen.helper.position import PositionHelperBase
from termsaverlib import common, exception, constants
from termsaverlib.i18n import _


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

    def __init__(self, name, description, url=None, tags=None,
                 print_format=None, delay=None, cli_opts=None):
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
        UrlFetcherBase.__init__(self,
            name, description, url, delay, cli_opts)

        XMLReaderHelperBase.__init__(self, "item", tags)

        self.print_format = print_format

        # build deafults
        if not cli_opts:
            self.cli_opts = {
                             'opts': 'hrd:u:f:',
                             'long_opts': ['raw', 'help', 'delay=',
                                           'url=', 'format=']
            }

        if not print_format:
            self.print_format = '%(title)s (%(pubDate)s)\n\n'

    def _usage_options_example(self):
        """
        Describe here the options and examples of this screen.

        The method `_parse_args` will be handling the parsing of the options
        documented here.

        Additionally, this is dependent on the values exposed in `cli_opts`,
        passed to this class during its instantiation. Only values properly
        configured there will be accepted here.
        """
        print _("""
Options:

 -h,  --help   Displays this help message
 -u,  --url    The URL path of the RSS feed (text) to be displayed
 -r,  --raw    Shows all text available (with HTML if any)
 -f, --format  The printing format according to values available in RSS feed:
                   * pubDate
                   * title
                   * link
                   * description
               You must use python dictionary based formatting style
               (see examples for details)

Example:

    $ %(app_name)s %(screen)s -u http://rss.cnn.com/rss/edition.rss
    This will trigger the screensaver to fetch the contents from the CNN feed
    and display it in default formatting: '%%(title)s (%%(pubDate)s)\\n'

    $ %(app_name)s %(screen)s -u http://rss.cnn.com/rss/edition.rss \\
        -f '%%(title)s (%%(pubDate)s)\\n%%(description)s\\n%%(link)s'
    This will trigger the screensaver to fetch the contents from the CNN feed
    and display all contents as specified in the formatting.
""") % {
        'app_name': constants.App.NAME,
        'screen': self.name,
        'description': self.description,
       }

    def _parse_args(self, prepared_args):
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

        for o, a in prepared_args[0]:  # optlist, args
            if o in ("-h", "--help"):
                self.usage()
                self.screen_exit()
            elif o in ("-r", "--raw"):
                self.clean_html = False
            elif o in ("-f", "--format"):
                #remove escaping
                self.print_format = common.unescape_string(a)
            elif o in ("-u", "--url"):
                try:
                    # try to fix the url formatting
                    self.url = self.fix_uri(a)
                except Exception, e:
                    raise exception.InvalidOptionException("url", e.message)
            else:
                # this should never happen!
                raise Exception(_("Unhandled option. See --help for details."))

        # last validations
        if self.url in (None, ''):
            raise exception.InvalidOptionException("url",
                "It is mandatory option", help=self._message_no_url())

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


class SimpleRSSFeedScreenBase(RSSFeedScreenBase):
    """
    Inherits the `RSSFeedScreenBase` class to handle basic RSS parsing.
    This will simplify the use of RSSFeedScreenBase by forcing a fixed
    URL feed, and simplify the code of screens inheriting from it.
    """

    def __init__(self, name, description, url, tags=None,
                 print_format=None, delay=None):
        """
        Creates a new instance of this class.

        This constructor has forced the url argument, compared with its base
        class, as it has no command line options to define its value manually
        """
        RSSFeedScreenBase.__init__(self,
                name, description, url, tags,
                 print_format, delay,
                 {'opts': 'h', 'long_opts': ['help']}
        )

    def _usage_options_example(self):
        """
        Describe here the options and examples of this screen.

        The method `_parse_args` will be handling the parsing of the options
        documented here.

        Additionally, this is dependent on the values exposed in `cli_opts`,
        passed to this class during its instantiation. Only values properly
        configured there will be accepted here.
        """
        print """
Options:

 -h,  --help   Displays this help message
"""

    def _parse_args(self, prepared_args):
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
        for o, __ in prepared_args[0]:  # optlist, args
            if o in ("-h", "--help"):
                self.usage()
                self.screen_exit()
            else:
                # this should never happen!
                raise Exception(_("Unhandled option. See --help for details."))
