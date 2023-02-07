###############################################################################
#
# file:     test.py
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

#
# Python built-in modules
#
import os
import sys
import unittest

#
# Import from parent path
#
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
    os.path.pardir)))

#
# Internal Modules (can only call this after the above PATH update)
#
from termsaver.termsaverlib.screen.helper import position


class PositionHelperTestCase(unittest.TestCase):

    p = None

    def setUp(self):
        self.p = position.PositionHelperBase()
        self.p.get_terminal_size()

    def testCenterHorizontallyText(self):

        # check no text
        t = ""
        self.p.center_text_horizontally(t)

        # test small word(s)
        t = "x"
        for __ in range(3):
            t += t
            nt = self.p.center_text_horizontally(t)
            self.assertEqual(nt.find(t),
                (self.p.geometry['x'] - len(t)) / 2)

        # test long word(s)
        t = "x" * 500
        for __ in range(3):
            t += t
            nt = self.p.center_text_horizontally(t)
            self.assertEqual(nt.find(t[0]), 0)

        # test multiple lines
        t = "\n".join(["x" * 25 for __ in range(10)])
        for __ in range(3):
            t += t
            nt = self.p.center_text_horizontally(t)

        # test long multiple lines
        t = "\n".join(["x" * 500 for __ in range(10)])
        for __ in range(3):
            t += t
            nt = self.p.center_text_horizontally(t)

    def testHorizontallyRandomizeText(self):

        # check no text
        t = ""
        self.p.randomize_text_horizontally(t)

        # test small word(s)
        t = "x"
        for __ in range(3):
            t += t
            self.p.randomize_text_horizontally(t)

        # test long word(s)
        t = "x" * 500
        for __ in range(3):
            t += t
            self.p.randomize_text_horizontally(t)

        # test multiple lines
        t = "\n".join(["x" * 25 for __ in range(10)])
        for __ in range(3):
            t += t
            self.p.randomize_text_horizontally(t)

        # test long multiple lines
        t = "\n".join(["x" * 500 for __ in range(10)])
        for __ in range(3):
            t += t
            self.p.randomize_text_horizontally(t)

    def testCenterVerticallyText(self):

        # check no text
        t = ""
        self.p.center_text_vertically(t)

        # test small word(s)
        t = "x"
        for __ in range(5):
            t += t
            nt = self.p.center_text_vertically(t)
            self.assertEqual(len(nt.split('\n')),
                (self.p.geometry['y'] - len(t.split('\n'))) / 2 + 1)
            self.assertEqual(len(nt.split('\n')) - 1, self.p.position['y'])

        # test long word(s)
        t = "x" * 500
        for __ in range(3):
            t += t
            self.p.center_text_vertically(t)

        # test multiple lines
        t = "\n".join(["x" * 25 for __ in range(10)])
        for __ in range(3):
            t += t
            self.p.center_text_vertically(t)

        # test long multiple lines
        t = "\n".join(["x" * 500 for __ in range(10)])
        for __ in range(3):
            t += t
            self.p.center_text_vertically(t)

#class CommonTestCase(unittest.TestCase):
#
#    path = '/tmp/temp-delete-ok'
#    file_count = 0
#    files_list = []
#    randomness = 10
#
#    def setUp(self):
#
#        unittest.TestCase.setUp(self)
#
#        #
#        # Create a recursive random directory tree for testing
#        #
#
#        # initialize values
#        self.file_count = 0
#        self.files_list = []
#
#        def create(path, count=1):
#            # create dummy files for testing
#            for i in range(count, self.randomness):
#                name = os.path.join(path, ''.join(random.choice(
#                        string.ascii_lowercase + string.digits) \
#                            for _ in range(5)))
#                if not os.path.exists(name):
#                    if random.random() > 0.5:  # 50% probability threshold
#                        os.makedirs(name)
#                        create(name, i)
#                    else:
#                        name += ".txt"
#                        f = open(name, "w")
#                        f.close()
#                        self.file_count += 1
#                        self.files_list.append(name)
#
#        if not os.path.exists(self.path):
#            os.makedirs(self.path)
#        else:
#            # force cleanup for s clean start
#            shutil.rmtree(self.path)
#
#        # randomize directories and files
#        create(self.path)
#
#    def tearDown(self):
#
#        unittest.TestCase.tearDown(self)
#
#        # clean up
#        shutil.rmtree(self.path)
#
#    def testRecurseToExec(self):
#
#        file_count = [0]  # muttable required for sub-function access
#
#        def count():
#            file_count[0] += 1
#
#        common.recurse_to_exec(self.path, count)
#
#        self.assertEqual(file_count[0], self.file_count)
#
#    def testRecurseToList(self):
#
#        files_list = common.recurse_to_list(self.path)
#
#        # sort lists for comparison
#        files_list.sort()
#        self.files_list.sort()
#
#        self.assertListEqual(files_list, self.files_list)


if __name__ == '__main__':
    unittest.main()
