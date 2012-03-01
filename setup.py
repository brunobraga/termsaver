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
The installation script of termsaver application. This also serves for
uninstallation, based on a previsouly created manifest file. See examples
below for details:

* Installation (simple)
    sudo python setup.py install

* Installation (build manifest)
    sudo python setup.py install --record /tmp/termsaver.install.record.txt

* Uninstallation
    sudo python setup.py uninstall --manifest /tmp/termsaver.install.record.txt

"""

import os
from distutils.core import setup
from distutils.cmd import Command
from distutils.log import warn, info
from distutils.errors import DistutilsFileError
from distutils.command.install_data import install_data
from distutils.command.build import build
from termsaverlib import constants


class Uninstall(Command):
    description = "Attempt an uninstall from an install --record file"

    user_options = [('manifest=', None, 'Installation record filename')]

    def initialize_options(self):
        self.manifest = None

    def finalize_options(self):
        pass

    def get_command_name(self):
        return 'uninstall'

    def run(self):
        f = None
        self.ensure_filename('manifest')
        try:
            try:
                if not self.manifest:
                        raise DistutilsFileError(
                            "Pass manifest with --manifest=file (previously \
created on install command with --record=file argument).")
                f = open(self.manifest)
                files = [p.strip() for p in f]
            except IOError, e:
                raise DistutilsFileError("unable to open install manifest: %s",
                                         str(e))
        finally:
            if f:
                f.close()

        for f in files:
            if os.path.isfile(f) or os.path.islink(f):
                info("removing %s" % repr(f))
                if not self.dry_run:
                    try:
                        os.unlink(f)
                    except OSError, e:
                        warn("could not delete: %s" % repr(f))
            elif not os.path.isdir(f):
                info("skipping %s" % repr(f))

        dirs = set()
        for f in reversed(sorted(files)):
            d = os.path.dirname(f)
            if d not in dirs and os.path.isdir(d) and len(os.listdir(d)) == 0:
                dirs.add(d)
                if d.find("site-packages") or d.find("dist-packages") > 0:
                    info("removing %s" % repr(d))
                    if not self.dry_run:
                        try:
                            os.rmdir(d)
                        except OSError, e:
                            warn("could not remove directory: %s" % str(e))
                else:
                    info("skipping empty directory %s" % repr(d))


class build_trans(Command):

    description = 'Compile .po files into .mo files'

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        po_dir = os.path.join(os.path.dirname(os.curdir), 'locale')
        for path, __, filenames in os.walk(po_dir):
            for f in filenames:
                if f.endswith('.po'):
                    lang = f[:len(f) - 3]
                    src = os.path.join(path, f)
                    dest_path = os.path.join('build', 'locale', lang,
                        'LC_MESSAGES')
                    dest = os.path.join(dest_path, 'termsaver.mo')
                    if not os.path.exists(dest_path):
                        os.makedirs(dest_path)
                    if not os.path.exists(dest):
                        print 'Compiling %s' % src
                        os.system("msgfmt %s -o %s" % (src, dest))
                    else:
                        src_mtime = os.stat(src)[8]
                        dest_mtime = os.stat(dest)[8]
                        if src_mtime > dest_mtime:
                            print 'Compiling %s' % src
                            os.system("msgfmt %s -o %s" % (src, dest))


class Build(build):

    sub_commands = build.sub_commands + [('build_trans', None)]

    def run(self):
        build.run(self)


class InstallData(install_data):

    def run(self):
        if not self.data_files: self.data_files = []
        for lang in os.listdir('build/locale/'):
            lang_dir = os.path.join('share', 'locale', lang, 'LC_MESSAGES')
            lang_file = os.path.join('build', 'locale', lang, 'LC_MESSAGES', 
                'termsaver.mo')
            self.data_files.append((lang_dir, [lang_file]))
            print 'Copying %s -> %s' % (lang_dir, lang_file)
        install_data.run(self)

setup(name='termsaver',
      version=constants.App.VERSION,
      description='Simple text-based terminal screensaver.',
      author='Bruno Braga',
      author_email='bruno.braga@gmail.com',
      url='http://termsaver.info',
      packages=[
            'termsaverlib',
            'termsaverlib.screen',
            'termsaverlib.screen.base',
            'termsaverlib.screen.helper',
      ],
      license='Apache License v2',
      scripts=['termsaver'],
      cmdclass={
                'build': Build,
                'build_trans': build_trans,
                'install_data': InstallData,
                'uninstall': Uninstall
      },
)


if __name__ == '__main__':
    #
    # The entry point of this application, as this should not be accessible as
    # a python module to be imported by another application.
    #
    print """Thank you for trying termsaver."""
