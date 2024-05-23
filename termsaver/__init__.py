#!/usr/bin/env python
###############################################################################
#
# file:     termsaver
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
The entry point script for termsaver application.

Usage: simplest form, just hit "termsaver" and go through
       the available options.

This script will basically handle simple parsing of arguments, also
transferring some of the arguments to a selected screen for additional and
customizable options.

See more details of this documentation in:

    * `usage` function
    * `parse_args` function
"""

import argparse
import errno
import random
#
# Python built-in modules
#
import sys
from signal import SIGINT, signal

from termsaver.termsaverlib import common, constants, exception
from termsaver.termsaverlib.helper.smartformatter import SmartFormatter
from termsaver.termsaverlib.helper.utilities import (hide_stdout_cursor,
                                                     show_stdout_cursor)
from termsaver.termsaverlib.i18n import _
#
# Internal modules
#
from termsaver.termsaverlib.screen import (build_screen_usage_list,
                                           get_available_screens)
from termsaver.termsaverlib.screen.base import ScreenBase
from termsaver.termsaverlib.screen.helper import ScreenHelperBase

verbose = False
"""
Defines if the error output should contain more debuging information.
The verbose mode here does not actually refer to printing logs on screen
(because this makes no sense for a screensaver), so any exceptions thrown that
kills the application will be just completely printed out for troubleshooting
purposes only.
"""

def usage():
    """
    Prints a simple description of termsaver, with a complete list of all
    available screens (installed in termsaverlib.screen package).
    """
    # Print the main termsaver header
    ScreenBase.usage_header()

    print (_("""Usage: %(app_name)s [screen] [options]

Screens:

 %(screens)s

Options:

 -h, --help     Displays this help message
 -v, --verbose  Displays python exception errors (for debugging)

Enhanced Features:
 * Install the following modules to enable enhanced features:
    * pynput - Enables the 'Press any key to exit' feature.
    * pygments - Colorizes the output of the Programmer screen.

Refer also to each screen's help by typing: %(app_name)s [screen] -h
""") % {
        'app_name': constants.App.NAME,
        'screens': build_screen_usage_list()
       })

    # Print the main termsaver footer
    ScreenBase.usage_footer()


def skip(arg = None):
    pass

def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    # if pygments is installed, reset the terminal colors to default
    try:
        from pygments import formatters
        print(formatters.TerminalFormatter().reset)
    except ImportError:
        pass
    show_stdout_cursor()
    sys.exit(0)
            
def entryPoint():
    signal(SIGINT, handler)
    hide_stdout_cursor()
    tscreen = getScreen()
    if tscreen:
        (screen, parser) = tscreen
        screen(parser=parser)._parse_args()
        

def getScreen():
    verbose = False
    use_random = False
    available_random_screens = [
        "asciiartfarts",
        "clocks",
        "jokes4all",
        "matrix",
        "quotes4all",
        "rfc",
        "starwars",
        "sysmon",
        "wttr"
    ]
    # if the operating system is windows, remove the sysmonscreen from the list of available screens
    if sys.platform == "win32":
        available_random_screens.remove("sysmon")

    try:
        # parse arguments and execute them accordingly

        # Set help parser with a custom formatter class (So we can use the line breaks and build_screen_usage_list())
        # Also, add_help removes the built-in help functionality from -h. 
        # We have to add it ourself, but it's customisable this way.
        parser = argparse.ArgumentParser(formatter_class=SmartFormatter,add_help=False, conflict_handler='resolve')
        # Adding parser arguments
        parser.add_argument("screen", type=str, action="store", default=None)
        parser.add_argument("-v", "--verbose",
                  action="store_true", dest="verbose", default=False,
                  help="Displays python exception errors (for debugging)")
        parser.add_argument("-h", "--help", action="store_true",dest="help",default=False)
        parser.add_argument("--random", action="store_true",dest="random",default=False)

        # Override the default format/help/error functions so we only see the information we want
        parser.format_usage = skip
        parser.format_help = skip
        parser.error = skip

        # Parse arguments into args we know of and args we don't.
        # We'll use this all over so the system can ignore arguments meant for specific screens.
        args, unkown = parser.parse_known_args()
        
        # Assign the important arguments on module init.
        verbose = True if args.verbose else False
        use_random = True if args.random else False
        if args.screen is None and args.random is None or (args.screen is None and args.random is None and args.help == True):
            usage()
            show_stdout_cursor()
            sys.exit(0)

        # Find the screen we're using and create it's parser as well as check validity with args.
        parsers = {}
        screenparsers = parser.add_subparsers()
        screen = None
        random_screen_name = None
        if use_random is True:
            random_screen_name = random.choice(available_random_screens)

        for s in get_available_screens():
            # Create the parsers for each screen.
            parsers[s.__name__.lower()] = screenparsers.add_parser(s.__name__.lower(), formatter_class=SmartFormatter, conflict_handler='resolve')
            if use_random is False:
                if s().name.lower() == args.screen:
                    screen = s
                    break
            elif use_random is True:
                if s().name.lower() == random_screen_name:
                    screen = s
                    break

        if screen == None:
            print(_("Invalid Screen."))
            usage()
            show_stdout_cursor()
            sys.exit(0)

        # Pass the parser to the selected screen.
        parser = parsers[screen.__name__.lower()]
        
        # Display usage if screen is select but help is requested.
        if (args.screen != None and args.help == True):
            screen(parser=parser).usage()
        else:
            #Go forth and parse args!
            return screen,parser
    except KeyboardInterrupt as e:
        #
        # Handles keyboard interrupt to exit this application
        # by cleaning up the screen for "left-overs"
        ScreenHelperBase.clear_screen()

        if verbose:
            common.prettify_exception(e)

        # Just finish gracefully
        show_stdout_cursor()
        sys.exit(0)

    except exception.TermSaverException as e:

        error_number = errno.EPERM  # 1

        if isinstance(e, exception.PathNotFoundException):
            #
            # Handles issues with file or directory reading errors
            #
            error_number = errno.ENOENT
            error_message = ""
            if hasattr(e, 'message'):
                error_message = e.message
            else:
                error_message = e
            
            print (_('Oops! Could not find path for %(path)s. %(msg)s') % \
                {'path': e.path, 'msg': error_message})

        elif isinstance(e, exception.InvalidOptionException):
            #
            # Handles issues with invalid options
            #
            error_number = errno.EINVAL
            error_message = ""
            if hasattr(e, 'message'):
                error_message = e.message
            else:
                error_message = e
            suf = ''

            if e.option_name not in (None, ''):
                suf = " '%s'" % e.option_name
            print (_('Oops! Invalid use of option%(suf)s. %(msg)s.%(help)s') % \
                {'suf': suf,
                 'msg': error_message,
                 'help': _(' See --help for details.')})

        elif isinstance(e, exception.UrlException):
            #
            # Handles issues with invalid URLs
            #
            error_number = errno.ENETUNREACH
            error_message = ""
            if hasattr(e, 'message'):
                error_message = e.message
            else:
                error_message = e

            print (_('Oops! Error while trying to fetch from %(url)s. %(msg)s')\
                 % {'url': e.url, 'msg': error_message})

        elif isinstance(e, exception.XmlException):
            #
            # Handles issues with invalid URLs
            #
            error_number = errno.ENOEXEC
            error_message = ""
            if hasattr(e, 'message'):
                error_message = e.message
            else:
                error_message = e

            suf = ''
            if e.name not in (None, ''):
                suf = " with '%s'" % e.name
            print (_('Oops! There were parsing issues%(suf)s. %(msg)s') % \
                {'suf': suf, 'msg': error_message})

        elif isinstance(e, exception.TermSaverException):
            #
            # Handles other termsaver errors
            #
            error_number = errno.ENOEXEC
            error_message = ""
            if hasattr(e, 'message'):
                error_message = e.message
            else:
                error_message = e

            print (_('Oops! There was an error: %(msg)s') % {'msg': error_message})

        if verbose:
            common.prettify_exception(e)

        if e.help_msg not in (None, ''):
            print(e.help_msg)

        show_stdout_cursor()
        sys.exit(error_number)

    except Exception as e:
        #
        # Handles keyboard interrupt to exit this application
        # by cleaning up the screen for "left-overs"
        #
        error_message = ""
        if hasattr(e, 'message'):
            error_message = e.message
        else:
            error_message = e

        print (_("""Oops! Something went terribly wrong.
Error details: %s""") % error_message)

        if verbose:
            common.prettify_exception(e)

        print (_("""
You are more than welcome to report this at:
        %(url)s
""") % {'url': constants.App.SOURCE_URL})

        if not verbose:
            print (_("""
Just before you do so, please run termsaver again with the
option --verbose and copy the output when you are filling
the bug report, that will help track faster the problem.
Thanks!
"""))
        show_stdout_cursor()
        sys.exit(errno.EPERM)
if __name__ == '__main__':
    #
    # The entry point of this application, as this should not be accessible as
    # a python module to be imported by another application.
    #
    entryPoint()
