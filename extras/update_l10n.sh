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

## ############################
## CONFIGURABLE SETTINGS: BEGIN
## ############################

#
# Defines the list of languages to be processed by this script, to
# (re)create and (re)compile the i18n (PO/MO) files located in 
#
langs="en ja pt"

#
# Defines the location of the i18n (PO/MO) files, 
# within the root path of this project
#
locale_path=locale

## ############################
## CONFIGURABLE SETTINGS: END
## ############################

#
# Exit on bash errors
#
set -o errexit

base_path="`pwd`/`dirname $0`/.."
cur_dir=`pwd`
locale_path="$base_path/$locale_path"

#
# Simple function to read properties from python,
# in this case, the termsaverlib.constants.App properties.
#
function get_prop() {
    python -c "from termsaverlib import constants as c; print c.App.$@"
}

cd $base_path

# remove build stuff (affects the seach here)
sudo rm -rfv build

for lang in $langs; do
    
    # create dir, if applicable
    d=$locale_path/$lang/LC_MESSAGES
    echo "Processing Language [$lang] ..."
    mkdir -p $d
    
    # create file if does not exist yet
    omit_header="--omit-header"
    new=0
    if [ ! -f $d/`get_prop "NAME"`.po ]; then   
        touch $d/`get_prop "NAME"`.po
        omit_header=
        new=1
    fi
    
    # process i18n
    echo "(Re)building PO file..."
    xgettext --language=Python \
             --no-wrap \
             --force-po \
             --join-existing \
             --keyword=_ \
             --force-po \
             $omit_header \
             --package-name="`get_prop "TITLE"`" \
             --package-version=`get_prop "VERSION"` \
             --output=$d/`get_prop "NAME"`.po \
             `find $base_path -iname "*.py" -or -iname "termsaver"`

    # for new files, replace the charset (to avoid warnings)
    if [ $new -eq 1 ]; then
        sed -i 's/charset=CHARSET/charset=utf-8/' $d/`get_prop "NAME"`.po
    fi
    
    # compile po
    echo "(Re)compiling MO file..."
    msgfmt $d/`get_prop "NAME"`.po -o $d/`get_prop "NAME"`.mo

done

# Done!
echo "Done"
