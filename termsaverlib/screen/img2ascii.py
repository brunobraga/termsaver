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
from termsaverlib.screen.base.imagereader import ImageReaderBase
from termsaverlib import constants
from termsaverlib.i18n import _

import os

class Img2Ascii(ImageReaderBase):
    """
    A simple screen that will display any text (hei programmer, source code!),
    on screen in a typing writer animation.

    From options available in `ImageReaderBase`, this will use:

        * `ImageReaderBase.cleanup_per_cycle` as True

        * `ImageReaderBase.cleanup_per_file` as True
    """


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
 -d, --delay        Sets the speed at which images will shift
                    Default is 1 second.
 -w, --wide         The width of each 'character' of the image.
                    Default is 2 units. (Recommended left at default)
 -c, --contrast     Displays image using a contrast based character set.
 -i, --invert       Displays the image with inverted colors.
 -s, --set          Allows the use of a custom character set.
                    Default is ' .:;+=xX$&'.
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
You just need to provide the path to the location from where %(app_title)s will
read and display on screen.

If you do not have any code in your local machine, just get some interesting
project from the Internet, such as Django (http://www.djangoproject.com):

    If you have access to git, you may download it at:
        git clone https://github.com/django/django.git

    Or, just download the zipped source and unpack it on your local machine:
        https://www.djangoproject.com/download/
""") % {
       'app_title': constants.App.TITLE,
    }


    def __init__(self):
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
        ImageReaderBase.__init__(self,
            "img2ascii",
            _("displays images in typing animation"),
            cli_opts={
                'opts': 'hicd:p:w:s:',
                'long_opts': ['help', 'invert', 'path=', 'wide=', 'contrast', 'set='],
            })
        self.cleanup_per_cycle = True
        self.cleanup_per_file = True
        self.options = {}

    def _parse_args(self, prepared_args):
        for o, a in prepared_args[0]:  # optlist, args
            if o in ("-h", "--help"):
                self.usage()
                self.screen_exit()
            elif o in ("-i", "--invert"):
                self.options['invert'] = True
            elif o in ("-w", "--wide"):
                try:
                    # makes sure this is a valid integer
                    self.options['wide'] = int(a)
                except:
                    raise exception.InvalidOptionException("wide")
            elif o in ("-c", "--contrast"):
                self.options['contrast'] = True
            elif o in ("-s", "--set"):
                self.options['customcharset'] = a
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