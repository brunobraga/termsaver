#!/bin/bash
###############################################################################
#
# file:     ubuntu_package.sh
#
# Purpose:  Prepares and builds DEB packages.
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
cur_dir=`pwd`

# precise oneiric hardy lucid natty
ubuntu_release=lucid

function get_prop() {
    python -c "from termsaverlib import constants; print constants.App.$@"
}


package_name=`get_prop "NAME"`
package_version=`get_prop "VERSION"`

temp_dir=/tmp/packaging/
package_dir_name=${package_name}_${package_version}

echo "Removing old garbage..."
rm -rfv $temp_dir
echo "Done"

echo "Creating temporary directory..."
mkdir -p $temp_dir
echo "Done"

echo "Copying project..."
cp -rfv $base_path $temp_dir/$package_dir_name
echo "Done"

cd  $temp_dir/$package_dir_name

echo "Cleaning up..."
rm -rfv .git*
echo "Done"

echo "Making original tarball"
mv debian ../
tar -czvf ../$package_dir_name.orig.tar.gz ../$package_dir_name
mv ../debian .
echo "Done"

# Fix stuff for Ubuntu
echo "Fixing Ubuntu stuff..."
# fix changelog
sed -i -s "s/($package_version-1) unstable/($package_version-ubuntu1) $ubuntu_release/" debian/changelog

# remove quilt
rm -rfv debian/source/format
echo "Done"

echo "Building package..."
#dpkg-buildpackage -rfakeroot
debuild -S # can not upload deb to launchpad, only sources
echo "Done"

cd $cur_dir

# Done!
echo "Finished packaging $package_dir_name"
