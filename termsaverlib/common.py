###############################################################################
#
# file:     common.py
#
# Purpose:  holds common helper functions used by termsaver code.
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
Holds common functionality used by termsaver screens.
"""

#
# Python build-in modules
#
import os
import sys
import traceback
import HTMLParser


def is_windows():
    """
    Returns True if the environment is Microsoft Windows.
    """
    return sys.platform == "win32"


def prettify_exception(ex):
    """
    Outputs the exception with its stack trace within separator lines.
    """
    print """
===================================
Exception: (%s) %s
%s
===================================
""" % (ex.__class__.__name__, ex.message, traceback.format_exc())


def get_app_dir():
    """
    Retrieves the termsaver main directory based on current operating system.

    For Windows machines, this should be something like:

        <root>\Documents and Settings\<user>\Application Data\termsaver

    For Unix machines, it will be:

        /home/<user>/.termsaver/
    """
    if is_windows():
        path = os.path.join(os.environ['APPDATA'], "termsaver")
    else:
        path = os.path.join(os.environ['HOME'], ".termsaver")

    # create if applicable
    if not os.path.exists(path):
        # permission errors here will just propagate error
        os.mkdir(path)

    return path


def get_temp_dir():
    """
    Retrieves the temporary based on current operating system.

    For Windows machines, this should be something like:

        <root>\Documents and Settings\<user>\Local Settings\Temp

    For Unix machines, it will be:

        /tmp/

    """
    if is_windows():
        path = os.environ['TMP']
    else:
        path = "/tmp"

    return path


def unescape_string(escaped_text):
    """
    Unescape strings. This is useful for cases when data that needs to be
    displayed on screen is escaped for HTML or database stuff.

    Additional replacing is taken here, such as some HTML tags:

        * <br>, replaced to \n
    """
    unescaped = escaped_text
    try:
        unescaped = HTMLParser.HTMLParser().unescape(escaped_text)
        unescaped = str(unescaped).lstrip().rstrip()
        # replace most common HTML data
        unescaped = unescaped.replace('<br>', '\n')
        unescaped = unescaped.replace('<br/>', '\n')
        unescaped = unescaped.replace('<br />', '\n')
        unescaped = unescaped.decode('string_escape')
    except:
        #
        # If there were errors here, just ignore them and try to give back
        # the string the best it could do
        #
        pass
    return unescaped


def get_day_suffix(day):
    """
    Returns the suffix of the day, such as in 1st, 2nd, ...
    """
    if day in (1, 11, 21, 31):
        return 'st'
    elif day in (2, 12, 22):
        return 'nd'
    elif day in (3, 13, 23):
        return 'rd'
    else:
        return 'th'
