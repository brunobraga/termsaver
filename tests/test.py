#import os
#import random
#import unittest
#import string
#import shutil
#
#import sys
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
#    os.path.pardir)))
#
#from termsaverlib import common


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
#
#
#if __name__ == '__main__':
#    unittest.main()
