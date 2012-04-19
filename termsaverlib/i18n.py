###############################################################################
#
# file:     i18n.py
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
Handles all internationalization (i18n) functionality for termsaver application
"""

#
# Python build-in modules
#
import gettext

#
# Internal modules
#
from termsaverlib import constants

_ = None
"""
The unicode text dealer for i18n stuff, renamed as an underscore to keep same
standards used by gettext.
"""


def set_app(application_name):
    """
    Defines the application name for the binding text files.
    """
    result = None

    try:
        gettext.textdomain(application_name)
        result = gettext.gettext
    except:
        #
        # If we can not handle i18n, just deal with text as it is
        #
        result = lambda x: x
    
        # For debugging
        #raise

    return result

#
# Call the default (termsaver app name)
#    
_ = set_app(constants.App.NAME)
#
# This should be overriden by plugins, as they can have their own i18n files
#