###############################################################################
#
# file:     constants.py
#
# Purpose:  refer to module documentation for details
#
# Note:     This file is part of Termsaver-Example plugin, and should not be
#           used or executed separately.
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
Holds constant values used throughout termsaver-exampleplugin plugin.
"""

#
# Termsaver modules
#
from termsaverlib.constants import PropertyClass


class Plugin(PropertyClass):
    """
    Holds application related properties used by termsaver-exampleplugin plugin
    screens. Refer to each of the available properties for detailed
    documentation.
    """

    VERSION = "0.1"
    """
    Defines the version of termsaver-exampleplugin plugin. This is accessed during
    install process, and to any help and usage messages informed by it.

    Refer to CHANGELOG file for a complete history about this project.
    """

    NAME = 'termsaver-exampleplugin'
    """
    Defines the termsaver-exampleplugin plugin, usually the plugin package name.
    """

    TITLE = 'TermSaver Example Plugin'
    """
    Defines the termsaver-exampleplugin plugin's official name as it should appear
    in documentation.
    """

    DESCRIPTION = 'A set of screens for showing an example termsaver plugin.'
    """
    Defines the main description of the termsaver-exampleplugin plugin.
    """

    URL = 'http://www.termsaver.info/plugins'
    """
    Defines the termsaver-exampleplugin plugin official website address.
    """

    SOURCE_URL = 'http://github.com/brunobraga/termsaver'
    """
    Defines the termsaver-exampleplugin plugin official source-code control site,
    hosted on GitHub.
    """

    AUTHORS = ['Bruno Braga <bruno.braga@gmail.com>']
    """
    Defines a list of all authors contributing to the termsaver-exampleplugin plugin.
    """


class Settings(PropertyClass):
    """
    Holds configuration settings used by termsaver-exampleplugin plugin. Refer to each
    of the available properties for detailed documentation.

    Follow the formatting:

    SETTING_NAME = VALUE
    \"\"\"
    document it!
    \"\"\"

    """
    pass
