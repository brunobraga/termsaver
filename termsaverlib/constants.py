###############################################################################
#
# file:     constants.py
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
Holds constant values used throughout termsaver application.
"""


class PropertyClass:
    """
    A base class that defines a class as a holder for properties only, not to
    be instantiated in any circumstances.
    """

    def __init__(self):
        """
        This class (and sub-classes) should not be instantiated.
        """
        raise NotImplementedError("This class cannot be instantiated!")


class App(PropertyClass):
    """
    Holds application related properties used by termsaver screens.
    Refer to each of the available properties for detailed documentation.
    """

    VERSION = "0.4"
    """
    Defines the version of termsaver application. This is accessed during
    install process, and to any help and usage messages informed by it.

    Refer to CHANGELOG file for a complete history about this project.
    """

    NAME = 'termsaver'
    """
    Defines the termsaver application, as it is executed from command-line.
    """

    TITLE = 'TermSaver'
    """
    Defines the termsaver application's official name as it should appear
    in documentation.
    """

    DESCRIPTION = 'A simple text-based terminal screensaver'
    """
    Defines the main description of the termsaver application.
    """

    URL = 'http://termsaver.brunobraga.net'
    """
    Defines the termsaver official website address.
    """

    SOURCE_URL = 'http://github.com/brunobraga/termsaver'
    """
    Defines the termsaver official source-code control site, hosted on GitHub.
    """

    AUTHORS = [
               'Bruno Braga <bruno.braga@gmail.com>',
               'Shelby Jueden <shelbyjueden@gmail.com>',
               'Alexander Riccio <alexander@riccio.com>',
    ]
    """
    Defines a list of all authors contributing to the termsaver application.
    """


class Settings(PropertyClass):
    """
    Holds configuration settings used by termsaver application. Refer to each
    of the available properties for detailed documentation.
    """

    CHAR_DELAY_SECONDS = 0.003
    """
    Defines basically the speed in which the text will be displayed, character
    by character, giving a cool impression of an automated type writing machine
    Default value is 0.003 seconds (3 milliseconds). It is advised to use
    values between 0.01 and 0.001.
    """

    FETCH_INTERVAL_SECONDS = 3600
    """
    Defines the interval between each fetching of data over the Internet.
    Default value is 1 hour.
    """
