###############################################################################
#
# file:     img2ascii.py
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
A screen to read source code files (or any other) in a  typing writer animation
See additional information in the class itself.

The helper class available here is:

    * `Img2Ascii`
"""
#
# Python built-in modules
#
import os
import queue
import time
from threading import Thread

#
# Internal modules
#
from termsaverlib.screen.base import ScreenBase
from termsaverlib.screen.helper.typing import TypingHelperBase
from termsaverlib.screen.helper.position import PositionHelperBase
from termsaverlib.screen.helper.imageconverter import ImageConverter
from termsaverlib import constants, exception
from termsaverlib.i18n import _

class Img2Ascii(ScreenBase, TypingHelperBase, PositionHelperBase):
    """
    A simple screen that will display any jpg or png image,
    on screen in a typing writer animation.
    """
    
    path = ''

    cleanup_per_file = False

    def _usage_options_example(self):
        """
        Describe here the options and examples of this screen.

        The method `_parse_args` will be handling the parsing of the options
        documented here.

        Additionally, this is dependent on the values exposed in `cli_opts`,
        passed to this class during its instantiation. Only values properly
        configured there will be accepted here.
        """
        print (_("""
Options:

 -p, --path         Sets the location to search for text-based source files.
                    This option is mandatory.
 -d, --delay        Sets the speed at which the image is typed out.
                    Default is 1 second. 
 -w, --wide         The width of each 'character' of the image.
                    Default is 2 units. (Recommended left at default)
 -c, --contrast     Displays image using a contrast based character set.
 -i, --invert       Displays the image with inverted colors.
 -s, --set          Allows the use of a custom character set.
                    Default is ' .:;+=xX$&'.
 -z, --scale        Scales the image.
                    Default is 1.
 -f, --framedelay   Sets the amount of time between image shifts.
                    Default is 5 seconds
 -h, --help         Displays this help message.

Examples:

    $ %(app_name)s %(screen)s -p /path/to/my/images
    This will trigger the screensaver to read all files in the path selected

    $ %(app_name)s %(screen)s -p /path/to/my/image.jpg
    This will trigger the screensaver to read just one image, refreshing at
    the preset interval.

    $ %(app_name)s %(screen)s -p /path/to/my/images -c -i
    This will trigger the screensaver to read all files in the path selected
    using a contrast characterset and inverted colors.

    $ %(app_name)s %(screen)s -p /path/to/my/images -s "1234567890_."
    This will trigger the screensaver to read all files in the path selected
    rendering them using only the characters provided.
    
""") % {
        'screen': self.name,
        'app_name': constants.App.NAME,
        'default_delay': constants.Settings.CHAR_DELAY_SECONDS,
    })


    def _message_no_path(self):
        """
        The specific helper message in case there is no path informed in the
        command-line arguments.
        """
        return _("""
You just need to provide the path to the image from where %(app_title)s will
read and display on screen.

You may also use online images by sending a url instead of image path.
""") % {
       'app_title': constants.App.TITLE,
    }


    def __init__(self, parser = None):
        """
        Creates a new instance of this class (used by termsaver script)

        From its base classes, the functionality provided here bases on the
        settings defined below:

            * clean up each cycle: True
              this will force the screen to be cleaned (cleared) before
              each new cycle is displayed

            * clean up each file: True
              this will force the screen to be cleaned (cleared) before
              each new file is displayed
        """
        ScreenBase.__init__(self,
            "img2ascii",
            _("displays images in typing animation"),
            parser
        )
        
        if self.parser:
            self.parser.add_argument("-p","--path", required=True, action="store", default=None, help="Sets the location to search for text-based source files.")
            self.parser.add_argument("-d","--delay",action="store", default=0.002, help="Sets the speed of the displaying characters.")
            self.parser.add_argument("-w","--wide",action="store", default=2, help="The width of each 'character' of the image.")
            self.parser.add_argument("-c","--contrast",action="store_true", default=False, help="Displays image using a contrast based character set.")
            self.parser.add_argument("-i","--invert",action="store_true", default=False, help="Displays the image with inverted colors.")
            self.parser.add_argument("-s","--set",action="store", default=' .:;+=xX$&', help="A string representing the character set to render with.")
            self.parser.add_argument("-z","--scale",action="store", default=1, help="Image Scale")
            self.parser.add_argument("-f","--framedelay",action="store", default=5, help="Sets the amount of time between images.")

        
        self.delay = 0.002
        self.frame_delay = 5
        # self.path = path
        self.cleanup_per_cycle = False
        self.options = {
            'invert':False,
            'wide':2,
            'contrast':False,
            'customcharset': ' .:;+=xX$&',
            'framedelay': self.frame_delay,
            'scale':1
        }
        self.cleanup_per_cycle = True
        self.cleanup_per_file = True

    def _parse_args(self, launchScreenImmediately=True):
        
        args, unknown = self.parser.parse_known_args()

        if args.invert:
            self.options['invert'] = True
        
        if args.wide:
            try:
                # makes sure this is a valid integer
                self.options['wide'] = int(args.wide)
            except:
                raise exception.InvalidOptionException("wide")
        
        if args.contrast:
            self.options['contrast'] = True
        
        if args.set:
            self.options['customcharset'] = args.set
            
        if args.framedelay:
            try:
                self.options['framedelay'] = int(args.framedelay)
            except:
                raise exception.InvalidOptionException("framedelay")
            
        if args.scale:
            try:
                self.options['scale'] = int(args.scale)
            except:
                raise exception.InvalidOptionException("scale")
        
        if args.delay:
            try:
                # make sure argument is a valid value (float)
                self.delay = float(args.delay)
            except:
                raise exception.InvalidOptionException("delay")
        
        if args.path:
            # make sure argument is a valid value (existing path)
            self.path = args.path
            if not os.path.exists(self.path) and self.path[0:4].lower() != 'http':
                raise exception.PathNotFoundException(self.path,
                    _("Make sure the file or directory exists."))
        
        if launchScreenImmediately:
            self.autorun()
        else:
            return self

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
        if not os.path.exists(self.path) and self.path[0:4] != 'http':
            raise exception.PathNotFoundException(self.path)

        queue_of_valid_files = queue.Queue()

        threads = [self.FileScannerThread(self, queue_of_valid_files, self.path)]
        threads[-1].daemon = True
        threads[-1].start()
        
        self.clear_screen()
        nextFile = queue_of_valid_files.get()
        while nextFile:
            self.get_terminal_size()
            imgconv = ImageConverter()
            file_data = imgconv.convert_image(nextFile, self.geometry['x'], self.geometry['y'], self.options)
            self.typing_print(file_data)
            time.sleep(self.frame_delay)
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
        print (_("""
Examples:

    $ %(app_name)s %(screen)s -p /path/to/images/
    This will trigger the screensaver to read all files in the path selected

    $ %(app_name)s %(screen)s -p /path/to/images/image.jpg -d 0
    This will trigger the screensaver to read all files in the path selected
    with no delay (too fast for a screensaver, but it's your choice that
    matters!)

    $ %(app_name)s %(screen)s -p /path/to/images/image.jpg -i -c
    This will trigger the screensaver to read the image from the internet and
    the image will be displayed in contrast mode and inverted.

    $ %(app_name)s %(screen)s -p http://website.com/image.jpg -d 5
    This will trigger the screensaver to read the image from the internet and
    display it extremely slowly
""") % {
        'screen': self.name,
        'app_name': constants.App.NAME,
    })

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
                    elif f.endswith(filetype) and self._is_path_binary(f):
                        func(f)
            elif path.endswith(filetype) and self._is_path_binary(path):
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
            Img2Ascii.recursively_populate_queue(self.__file_reader_instance, self.__queue_of_valid_files, self.__path_to_scan)
