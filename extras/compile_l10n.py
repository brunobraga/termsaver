#!/usr/bin/env python
###############################################################################
#
# file:     compile_l10n.py
#
# Purpose:  Recreate MO files for localization.
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

import os
import sys


def main():

    print "Starting to compile available l10n messages..."
    po_dir = os.path.join(sys.path[0], '..', 'locale')
    for lang in os.listdir(po_dir):

        lang_path = os.path.join('locale', lang, 'LC_MESSAGES')
        src = os.path.join(lang_path, 'termsaver.po')
        dest = os.path.join(lang_path, 'termsaver.mo')
        print 'Compiling %s' % src
        if os.system("msgfmt %s -o %s" % (src, dest)) != 0:
            print "Error while compiling file!"
            sys.exit(2)

    print "Done!"


if __name__ == '__main__':
    #
    # The entry point of this application, as this should not be accessible as
    # a python module to be imported by another application.
    #
    main()
