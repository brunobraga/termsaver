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
import Queue as queue
from threading import Thread

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

        * `delay`: Defines the speed of the typing writer. See more details
          of this in `TypingHelperBase` class documentation. Its value is
          defined by `TypingHelperBase`'s default, if none is informed.

        * `path`: Defines the path to be recursively checked for text
                  files to be displayed on terminal screen.

    When inheriting from this screen, you can also take advantage of the
    following properties and functionalities:

        * `cleanup_per_file`: forces to clean up the screen for each file in
          the looping. The alternative, available in
          `ScreenBase.cleanup_per_cycle`, only handles a cycle action.

    """

    path = ''

    cleanup_per_file = False

    def __init__(self, name, description, path=None, delay=None, cli_opts=None):
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
        # define default cli options, if none are informed
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
        Executes a \"cycle\" of this screen.
            * The concept of \"cycle\" is no longer accurate, and is misleading.
              this function will not return.
        New threaded implementation:
            * Checks if self.path is a valid path, using `os.path.exists`
            * Assigns a new Queue to `queue_of_valid_files`
            * Appends a new `FileScannerThread` object to a list of threads
            * `start()`s the `FileScannerThread`
                * `FileScannerThread` will put paths in the queue as valid
                   file paths are found
            * `clear_screen()`s
            * Gets a file from `queue_of_valid_files`, removing item from queue
            * While nextFile (empty sequences are false)
                * As long as there is something in the queue - that is, as long
                  as `queue.queue.get()` is able to get an object from (the)
                  `queue_of_valid_files`, this test evaluates True.
                * I imagine that this behaves unpredictably given a computer
                  with __REALLY__ slow I/O
            * Opens `nextFile` with handle-auto-closing `with` statement and
              `typing_print()`s it
            * Clears screen if `self.cleanup_per_file`
            * Puts `nextFile` ON the queue
                * Because `queue_of_valid_files.get()` REMOVES a file path
                  from the queue, `_run_cycle()` will never reach that path
                  again, and eventually will exhaust the queue
                  (failing silently, with a blank screen)
                    * A static blank screen is the antithesis of a screensaver
                * Therefore, `queue_of_valid_files.put(nextFile)` puts the file
                  path at the last spot in the queue
            * Finally, another call to `queue_of_valid_files.get()` sets up
              the next iteration in the while loop.
        """
        # validate path
        if not os.path.exists(self.path):
            raise exception.PathNotFoundException(self.path)

        queue_of_valid_files = queue.Queue()

        threads = [FileReaderBase.FileScannerThread(self, queue_of_valid_files, self.path)]
        threads[-1].daemon = True
        threads[-1].start()
        #self.clear_screen() hides any error message produced before it!
        self.clear_screen()
        nextFile = queue_of_valid_files.get()
        while nextFile:
            with open(nextFile, 'r') as f:
                file_data = f.read()
                self.typing_print(file_data)
            if self.cleanup_per_file:
                self.clear_screen()
            queue_of_valid_files.put(nextFile)
            nextFile = queue_of_valid_files.get()
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
                    if os.path.isdir(f):
                        if not item.startswith('.'):
                            self._recurse_to_exec(f, func, filetype)
                    elif f.endswith(filetype) and not self._is_path_binary(f):
                        func(f)
            elif path.endswith(filetype) and not self._is_path_binary(path):
                func(path)
        except:
            # If IOError, don't put on queue, as the path might throw
            # another IOError during screen saver operations.
            return

    @staticmethod
    def recursively_populate_queue(self, queue_of_valid_files, path, filetype=''):
        """
        Populates an (empty) queue of all files within directory
        in "path", with the paths to said files.

        MUST be a staticmethod for threaded implementation to function.

        Arguments:
            * queue_of_valid_files

            * path: the path to be recursively checked (directory)

            * filetype: to filter for a specific filetype
        """
        self._recurse_to_exec(path, queue_of_valid_files.put, filetype)

    def _is_path_binary(self, path):
        """
        Returns True if the given path corresponds to a binary, or, if for any
        reason, the file can not be accessed or opened.

        For the merit of being a binary file (i.e., termsaver will not be able
        to handle it), it is safe enough to consider the above True, as any
        files in this situation will be simply skipped, avoiding weird errors
        being thrown to the end-user.

        Arguments:

            * path: the file location
        """
        CHUNKSIZE = 1024

        f = None
        try:
            f = open(path, 'rb')
        except:
            # If IOError, don't even bother, as the path might throw
            # another IOError during screen saver operations.
            return True
        try:
            while True:
                chunk = f.read(CHUNKSIZE)
                if '\0' in chunk:  # found null byte
                    return True
                if len(chunk) < CHUNKSIZE:
                    break  # done
        except:
            # If IOError, don't even bother, as the path might throw
            # another IOError during screen saver operations.
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

    class FileScannerThread(Thread):
        """Screen-animation independent thread for path scanning.
           Allows animation to begin prior to completion of path scanning.
        """
        def __init__(self, fileReaderInstance, queue_of_valid_files, path_to_scan):
            Thread.__init__(self)
            self.__queue_of_valid_files = queue_of_valid_files
            self.__path_to_scan         = path_to_scan
            self.__file_reader_instance = fileReaderInstance
        def run(self):
            """Thread begins executing this function on
               call to `aThreadObject.start()`.
            """
            FileReaderBase.recursively_populate_queue(self.__file_reader_instance, self.__queue_of_valid_files, self.__path_to_scan)
