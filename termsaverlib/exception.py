###############################################################################
#
# file:     exceptions.py
#
# Purpose:  holds termsaver special exceptions
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
This module holds special exceptions triggered by termsaver (and handled
internally as well, but with more human-readable treatment).

The classes available here are:

  * `TermSaverException`
     A generic exception that implements read-only functionality for its
     inheriting classes.

  * `ScreenNotFoundException`
     An exception that happens when termsaver is dealing with non existing
     screens.

  * `PathNotFoundException`
     An exception that happens when termsaver is dealing with non existing
     files.

  * `UrlException`
     An exception that happens when termsaver is dealing with URL connectvitiy
     issues.

"""


class TermSaverException(Exception):
    """
    A base exception class providing additional read-only feature to its
    inheriting classes. You must fill the `readonly` list to enable a property
    as read-only.
    """

    readonly = []
    """
    Defines a list to place names of properties that should be read-only.
    """

    help_msg = ''
    """
    An extra string of information to help guide users on exception issues.
    """

    def __init__(self, *args, **kwargs):
        """
        Instantiate a new exception object.

        You may use the extra property `help` when instantiating this.
        """

        Exception.__init__(self, *args)

        # get the help argument dynamically from kwargs, if applicable
        if "help" in kwargs:
            self.help_msg = kwargs['help']

            # mark this property as read-only
            self.readonly.append("help")

    def __setattr__(self, name, val):
        """
        Override of original to check for read-only properties, throwing
        exception if tempered with.
        """
        if name not in self.readonly:
            self.__dict__[name] = val
        else:
            raise Exception("%s.%s is read only!" % (self.__class__.__name__,
                                                     name))


class PathNotFoundException(TermSaverException):
    """
    Exception to handle special cases when a path required to run could not be
    found in the file system.
    """

    path = ''
    """
    The name of the screen that could not be found by termsaver.
    """

    def __init__(self, path, *args, **kwargs):
        """
        Instantiates this exception class, with an additional parameter for the
        name of the screen not found by termsaver. This value is accessible by
        """
        TermSaverException.__init__(self, *args, **kwargs)
        self.path = path

        # mark this property as read-only
        self.readonly.append('path')


class UrlException(TermSaverException):
    """
    Exception to handle special cases when connectivity to a specific URL was
    not successful.
    """

    url = ''
    """
    The name of the screen that could not be found by termsaver.
    """

    def __init__(self, url, *args, **kwargs):
        """
        Instantiates this exception class, with an additional parameter for the
        name of the screen not found by termsaver. This value is accessible by
        """
        TermSaverException.__init__(self, *args, **kwargs)
        self.url = url

        # mark this property as read-only
        self.readonly.append('url')


class InvalidOptionException(TermSaverException):
    """
    Exception to handle special cases when user uses comman line options
    wrongfully.
    """

    option_name = ''
    """
    The name of the screen that could not be found by termsaver.
    """

    def __init__(self, option_name, *args, **kwargs):
        """
        Instantiates this exception class, with an additional parameter for the
        name of the screen not found by termsaver. This value is accessible by
        """
        TermSaverException.__init__(self, *args, **kwargs)
        self.option_name = option_name

        # mark this property as read-only
        self.readonly.append('option_name')


class XmlException(TermSaverException):
    """
    Exception to handle XML issues.
    """

    name = ''
    """
    The name of the file path or URL that had issues with parsing
    """

    def __init__(self, name, *args, **kwargs):
        """
        Instantiates this exception class, with an additional parameter for the
        name of the screen not found by termsaver. This value is accessible by
        """
        TermSaverException.__init__(self, *args, **kwargs)
        self.name = name

        # mark this property as read-only
        self.readonly.append('name')
