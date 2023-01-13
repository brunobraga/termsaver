###############################################################################
#
# file:     __init__.py
#
# Purpose:  refer to module documentation for details
#
# Note:     This file is part of Termsaver-ExamplePlugin plugin, and should not be used
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
This module holds base classes that are used by all screens within termsaver
application. Each individual "screen" represents a unique screensaver that can
be triggered by termsaver.

The base classes available in this package are:

  * `ExamplePluginScreenBase`: the most basic screen class, which will handle simple
     interaction with the terminal.


"""

#
# Python built-in modules
#
import os
import textwrap

from termsaver.termsaverlib import common, exception
from termsaver.termsaverlib.i18n import _, set_app
#
# Internal modules
#
from termsaver.termsaverlib.screen.base import ScreenBase
from termsaver.termsaverlib.screen.helper.position import PositionHelperBase

#
# Override termsavr default i18n (reuired for plugins with own i18n files)
#
set_app("termsaver-exampleplugin")

class ExamplePluginScreenBase(ScreenBase, PositionHelperBase):
  """
  """

  def example_echo(self, echo_text):
    """
    Just echos the incoming text
    """
    return echo_text
