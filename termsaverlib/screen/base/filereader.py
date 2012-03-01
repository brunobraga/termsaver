###############################################################################
#
# file:     filereader.py
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
This module contains a screen base class that handles screens that require
recursive directory scanning for files to be printed out.
See additional information in the class itself.

The helper class available here is:

    * `FileReaderBase`
"""

#
# Python built-in modules
#
import os

#
# Internal modules
#
from termsaverlib.screen.base import ScreenBase
from termsaverlib import exception, constants
from termsaverlib.screen.helper.typing import TypingHelperBase
from termsaverlib.i18n import _


class FileReaderBase(ScreenBase, TypingHelperBase):
    """
    A base class used to handle file reading, more specifically, multiple files
    retrieved from a `path` recursively. This also uses the `TypingHelperBase`
    helper class to add functionality of typing writer display.

    The instantiation of this class takes two additional arguments, compared
    with its base class:

        * `delay`: defines the speed of the typing writer. See more details
          of this in `TypingHelperBase` class documentation. Its value is
          defined by `TypingHelperBase`'s default, if none is informed.

        * `path`: defines the path from where this screen should scan
          for files

    When inheriting from this screen, you can also take advantage of the
    following properties and functionalities:

        * `cleanup_per_file`: forces to clean up the screen for each file in
          the looping. The alternative, available in
          `ScreenBase.cleanup_per_cycle`, only handles a cycle action.

    """

    path = ''
    """
    Defines the path to be recursively checked for text files to be displayed
    on terminal screen.
    """

    cleanup_per_file = False
    """
    Defines if termsaver should clean the screen for each file being read
    """

    def __init__(self, name, description, path=None,
                 delay=None, cli_opts=None):
        """
        Creates a new instance of this class.

        This constructor has two additional arguments, compared with its base
        class:

            * delay: defines the speed of the typing writer. See more details
              of this in `TypingHelperBase` class documentation.

            * path: defines the path from where this screen should scan
              for files
        """
        ScreenBase.__init__(self, name, description, cli_opts)
        # define default cli options, if none is informed
        if not cli_opts:
            self.cli_opts = {
                             'opts': 'hd:p:',
                             'long_opts': ['help', 'delay=', 'path='],
            }
        self.delay = delay
        self.path = path
        self.cleanup_per_cycle = False

    def _run_cycle(self):
        """
        Executes a cycle of this screen.

        The actions taken here, for each cycle, are as follows:

            * loop all files retrieved from `path`
            * open each file, read its contents
            * print using `typing_print`
        """
        # validate path
        if not os.path.exists(self.path):
            raise exception.PathNotFoundException(self.path)

        # get the list of available files
        file_list = self._recurse_to_list(self.path)

        if len(file_list) == 0:
            raise exception.PathNotFoundException(self.path)

        self.clear_screen()
        for path in file_list:
            f = open(path, 'r')

            # read the file with the typing feature
            self.typing_print(f.read())
            f.close()

            if self.cleanup_per_file:
                self.clear_screen()

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

 -p, --path   Sets the location to search for text-based source files.
              this option is mandatory.
 -d, --delay  Sets the speed of the displaying characters
              default is%(default_delay)s of a second
 -h, --help   Displays this help message

Examples:

    $ %(app_name)s %(screen)s -p /path/to/my/code
    This will trigger the screensaver to read all files in the path selected

    $ %(app_name)s %(screen)s -p /path/to/my/code -d 0
    This will trigger the screensaver to read all files in the path selected
    with no delay (too fast for a screensaver, but it's your choice that
    matters!)
""") % {
        'screen': self.name,
        'app_name': constants.App.NAME,
        'default_delay': constants.Settings.CHAR_DELAY_SECONDS,
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
            elif o in ("-d", "--delay"):
                try:
                    # make sure argument is a valid value (float)
                    self.delay = float(a)
                except:
                    raise exception.InvalidOptionException("delay")
            elif o in ("-p", "--path"):
                # make sure argument is a valid value (existing path)
                self.path = a
                if not os.path.exists(self.path):
                    raise exception.PathNotFoundException(self.path,
                        _("Make sure the file or directory exists."))
            else:
                # this should never happen!
                raise Exception(_("Unhandled option. See --help for details."))

        # last validations
        if self.path in (None, ''):
            raise exception.InvalidOptionException("path",
                _("It is mandatory option"), help=self._message_no_path())

    def _recurse_to_exec(self, path, func, filetype=''):
        """
        Executes a function for each file found recursively within the
        specified path.

        Arguments:

            * path: the path to be recursively checked (directory)

            * func: the function to be executed with the file(s)

            * filetype: to filter for a specific filetype
        """
        try:
            if os.path.isdir(path):
                for item in os.listdir(path):
                    f = os.path.join(path, item)
                    self.log("checking %s..." % f)
                    if os.path.isdir(f):
                        if not item.startswith('.'):
                            self._recurse_to_exec(f, func, filetype)
                    elif f.endswith(filetype) and not self._is_path_binary(f):
                        func(f)
            elif path.endswith(filetype) and not self._is_path_binary(path):
                func(path)
        except:
            #
            # In case of IOErrors, assume this is true for simplicity reasons
            # as the file should be ignored for screen saver operations.
            #
            return

    def _recurse_to_list(self, path, filetype=''):
        """
        Returns a list of all files within directory in "path"

        Arguments:

            * path: the path to be recursively checked (directory)

            * filetype: to filter for a specific filetype
        """
        result = []
        self._recurse_to_exec(path, result.append, filetype)
        return result

    def _is_path_binary(self, path):
        """
        Returns True if the given path corresponds to a binary, or, if by an
        reason, the file can not be accessed or opened.

        For the merit of being a binary file (i.e., termsaver will not be able
        to handle it), it is safe enough to consider the above True, as any
        files in this situation will be simply skipped, avoiding weird errors
        being thrown to the end-user.

        Arguments:

            path: the file location
        """
        CHUNKSIZE = 1024

        f = None
        try:
            f = open(path, 'rb')
        except:
            #
            # In case of IOErrors, assume this is true for simplicity reasons
            # as the file should be ignored for screen saver operations.
            #
            return True
        try:
            while True:
                chunk = f.read(CHUNKSIZE)
                if '\0' in chunk:  # found null byte
                    return True
                if len(chunk) < CHUNKSIZE:
                    break  # done
        except:
            #
            # In case of IOErrors, assume this is true for simplicity reasons
            # as the file should be ignored for screen saver operations.
            #
            return True
        finally:
            if f:
                f.close()
        return False

    def _message_no_path(self):
        """
        Defines a method to be overriden by inheriting classes, with the
        purpose to display extra help information for specific errors.
        """
        return ""
