###############################################################################
#
# file:     smartformatter.py
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
import argparse
import sys

class SmartFormatter(argparse.ArgumentDefaultsHelpFormatter):

    def _split_lines(self, text, width):

        if text.startswith('R|'):
            text = text[2:]
            return text.split_lines(self,text,width)

        return argparse.ArgumentDefaultsHelpFormatter._split_lines(self, text, width)
