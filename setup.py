#!/usr/bin/env python
###############################################################################
#
# file:     setup.py
#
# Purpose:  installs the termsaver application
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
The installation script of termsaver application.

    sudo python setup.py install

    # For debian based installation style
    sudo ./setup.py install --install-lib=/usr/local/share/termsaver --install-scripts=/usr/local/share/termsaver --install-data=/usr/local
    sudo ln -s /usr/local/share/termsaver/termsaver /usr/local/bin/termsaver

You may also refer to:

    sudo pip install termsaver

"""

import os
import platform
from distutils.core import setup
from termsaverlib import constants


if platform.system() == 'FreeBSD':
    man_dir = 'man'
else:
    man_dir = 'share/man'

data_files = [(os.path.join('share', 'locale', lang, 'LC_MESSAGES'),
                [os.path.join('locale', lang, 'LC_MESSAGES',
                'termsaver.mo')]) for lang in os.listdir('locale')]
data_files.append((os.path.join(man_dir, 'man1'), ['doc/termsaver.1']))
data_files.append(('etc/bash_completion.d',
                   ['completion/termsaver-completion.bash']))
data_files.append(('share/zsh/site-functions', ['completion/_termsaver']))

setup(name='termsaver',
      version=constants.App.VERSION,
      description='Simple text-based terminal screensaver.',
      author='Bruno Braga',
      author_email='bruno.braga@gmail.com',
      classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: Information Technology',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: Apache Software License',
            'Natural Language :: English',
            'Operating System :: MacOS',
            'Operating System :: POSIX',
            'Programming Language :: Python',
            'Topic :: Terminals',
            'Topic :: Utilities',
      ],
      url='http://termsaver.brunobraga.net',
      keywords=['command-line', 'terminal', 'screensaver'],
      packages=[
            'termsaverlib',
            'termsaverlib.plugins',
            'termsaverlib.screen',
            'termsaverlib.screen.base',
            'termsaverlib.screen.helper',
      ],
      license='Apache License v2',
      scripts=['termsaver'],
      data_files=data_files,
)


if __name__ == '__main__':
    #
    # The entry point of this application, as this should not be accessible as
    # a python module to be imported by another application.
    #
    print """
Thank you for trying termsaver.
"""
