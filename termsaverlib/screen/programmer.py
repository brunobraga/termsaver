###############################################################################
#
# file:     programmer.py
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

    * `ProgrammerScreen`
"""
from termsaverlib.screen.base.filereader import FileReaderBase
from termsaverlib import constants, exception
from termsaverlib.i18n import _
from argparse import ArgumentParser


class ProgrammerScreen(FileReaderBase):
    """
    A simple screen that will display any text (hei programmer, source code!),
    on screen in a typing writer animation.

    From options available in `FileReaderBase`, this will use:

        * `FileReaderBase.cleanup_per_cycle` as True

        * `FileReaderBase.cleanup_per_file` as True
    """

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
        FileReaderBase.__init__(self,
            "programmer",
            _("displays source code in typing animation (with pygments support)"))
            parser
        )

        self.cleanup_per_cycle = True
        self.cleanup_per_file = True
        self.colorize = True
        self.ignore_binary = True

    def _parse_args(self):
        """
        Handles the special command-line arguments available for this screen.
        Although this is a base screen, having these options prepared here
        can save coding for screens that will not change the default options.

        Additionally, this is dependent on the values exposed in `cli_opts`,
        passed to this class during its instantiation. Only values properly
        configured there will be accepted here.
        """
        args, unknown = self.parser.parse_known_args()
        
        # last validations
        if args.path in (None, ''):
            raise exception.InvalidOptionException("path",
                _("It is mandatory option"), help=self._message_no_path())
        else:
            self.path = args.path
        
        if args.delay:
            self.delay = args.delay
        else:
            self.delay = constants.Settings.CHAR_DELAY_SECONDS
        
        self.autorun()

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
