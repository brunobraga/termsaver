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
from termsaverlib import constants
from termsaverlib.i18n import _


class ProgrammerScreen(FileReaderBase):
    """
    A simple screen that will display any text (hei programmer, source code!),
    on screen in a typing writer animation.

    From options available in `FileReaderBase`, this will use:

        * `FileReaderBase.cleanup_per_cycle` as True

        * `FileReaderBase.cleanup_per_file` as True
    """

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
        FileReaderBase.__init__(self,
            "programmer",
            _("displays source code in typing animation"))
        self.cleanup_per_cycle = True
        self.cleanup_per_file = True

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
