#!/bin/bash
###############################################################################
#
# file:     update_l10n.sh
#
# Purpose:  Rebuild localization po files.
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

base_path="`pwd`/`dirname $0`/.."
locale_path="$base_path/locale"
langs="en ja pt"

function get_prop() {
    python -c "from termsaverlib import constants; print constants.App.$@"
}

for lang in $langs; do
    echo "processing $locale_path/$lang.po ..."
    touch $locale_path/$lang.po
    xgettext --language=Python \
             --no-wrap \
             --force-po \
             --join-existing \
             --keyword=_ \
             --force-po \
             --omit-header \
             --package-name=`get_prop "TITLE"` \
             --package-version=`get_prop "VERSION"` \
             --output=$locale_path/$lang.po \
             `find $base_path -iname "*.py" -or -iname "termsaver"`
done

# Done!
echo "Done"
