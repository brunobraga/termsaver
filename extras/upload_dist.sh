#!/bin/bash
###############################################################################
#
# file:     upload_dist.sh
#
# Purpose:  Upload this application to Python distribution channel.
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

echo "Cleaning up previous actions..."
rm -rvf ./README ./dist ./build ./MANIFEST termsaver.egg-info/

#
# Bring the dist README file for uploading process
#
echo "Copying distribution README file to root directory..."
cp -vf extras/README.dist ./README

echo "Executing python source distribution upload..."
python setup.py sdist upload

# Done!
echo "Done"
