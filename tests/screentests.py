import unittest
import sys
import os
import argparse
import time

bin_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.abspath(bin_path)
par_path = os.path.abspath(os.path.join(lib_path,os.path.pardir))
sys.path.insert(0, lib_path)
sys.path.insert(0, par_path)

import termsaver
from termsaverlib import constants
from termsaverlib.exception import InvalidOptionException, PathNotFoundException

class ScreenTestCase(unittest.TestCase):
    screenName = ""
    def getScreen(self, args = []):
        sys.argv = ['termsaver.py', self.screenName]
        sys.argv.extend(args)
        screen,parser = termsaver.getScreen()
        return screen(parser=parser)._parse_args(False)

class ClockScreen_TestCase(ScreenTestCase):

    screenName = "clock"

    def test_ampm(self):
        screen = self.getScreen()
        self.assertEqual(screen.ampm, False)
                
        screen = self.getScreen( ['-m'])
        self.assertEqual(screen.ampm, True)
        
    def test_big(self):
        screen = self.getScreen()
        self.assertEqual(screen.big, False)
                
        screen = self.getScreen( ['-b'])
        self.assertEqual(screen.big, True)
            
    def test_all(self):
        screen = self.getScreen()
        self.assertEqual(screen.big, False)
        self.assertEqual(screen.ampm, False)
                
        screen = self.getScreen( ['-mb'])
        self.assertEqual(screen.big, True)
        self.assertEqual(screen.ampm, True)

class Img2AsciiScreen_TestCase(ScreenTestCase):
    screenName = "img2ascii"
    required_args = ['-p', './empty-for-tests']
    
    def test_path(self):
        with self.assertRaises(SystemExit):
            self.getScreen()
        with self.assertRaises(PathNotFoundException):
            self.getScreen(['-p', './nonexistant-directory'])
        try:
            self.getScreen(self.required_args)
        except PathNotFoundException:
            self.fail("Testing for valid pathing failed.")
        
    def test_delay(self):
        screen = self.getScreen(self.required_args)
        self.assertEqual(screen.delay, 0.002)

        targs = self.required_args.copy()
        targs.extend(['-d', '0.1'])
        screen = self.getScreen(targs)
        self.assertEqual(screen.delay, 0.1)
        
    def test_invert(self):
        screen = self.getScreen(self.required_args)
        self.assertEqual(screen.options['invert'], False)
        targs = self.required_args.copy()
        targs.extend(['-i'])
        screen = self.getScreen(targs)
        self.assertEqual(screen.options['invert'], True)
        
    def test_wide(self):
        screen = self.getScreen(self.required_args)
        self.assertEqual(screen.options['wide'], 2)
        targs = self.required_args.copy()
        targs.extend(['-w','4'])
        screen = self.getScreen(targs)
        self.assertEqual(screen.options['wide'], 4)

    def test_contrast(self):
        screen = self.getScreen(self.required_args)
        self.assertEqual(screen.options['contrast'], False)
        targs = self.required_args.copy()
        targs.extend(['-c'])
        screen = self.getScreen(targs)
        self.assertEqual(screen.options['contrast'], True)
        
    def test_customcharset(self):
        screen = self.getScreen(self.required_args)
        self.assertEqual(screen.options['customcharset'], ' .:;+=xX$&')
        targs = self.required_args.copy()
        targs.extend(['-s','abcdefg'])
        screen = self.getScreen(targs)
        self.assertEqual(screen.options['customcharset'], 'abcdefg')

    def test_framedelay(self):
        screen = self.getScreen(self.required_args)
        self.assertEqual(screen.options['framedelay'], 5)
        targs = self.required_args.copy()
        targs.extend(['-f','3'])
        screen = self.getScreen(targs)
        self.assertEqual(screen.options['framedelay'], 3)
        
    def test_scale(self):
        screen = self.getScreen(self.required_args)
        self.assertEqual(screen.options['scale'], 1)
        targs = self.required_args.copy()
        targs.extend(['-z','3'])
        screen = self.getScreen(targs)
        self.assertEqual(screen.options['scale'], 3)

    def test_all(self):
        screen = self.getScreen(self.required_args)
        self.assertEqual(screen.delay, 0.002)
        self.assertEqual(screen.options['invert'], False)
        self.assertEqual(screen.options['wide'], 2)
        self.assertEqual(screen.options['contrast'], False)
        self.assertEqual(screen.options['customcharset'], ' .:;+=xX$&')
        self.assertEqual(screen.options['framedelay'], 5)
        self.assertEqual(screen.options['scale'], 1)
        
        targs = self.required_args.copy()
        targs.extend(['-ic','-d','1','-w','1','-f','1','-z','2','-s','abc123'])
        screen = self.getScreen(targs)
        self.assertEqual(screen.delay, 1)
        self.assertEqual(screen.options['invert'], True)
        self.assertEqual(screen.options['wide'], 1)
        self.assertEqual(screen.options['contrast'], True)
        self.assertEqual(screen.options['customcharset'], 'abc123')
        self.assertEqual(screen.options['framedelay'], 1)
        self.assertEqual(screen.options['scale'], 2)

class Jokes4AllScreen_TestCase(ScreenTestCase):

    screenName = "jokes4all"
            
    def test_delay(self):
        screen = self.getScreen()
        self.assertEqual(screen.sleep_between_items, 30)

        targs = ['-d', '1']
        screen = self.getScreen(targs)
        self.assertEqual(screen.sleep_between_items, 1)

class Quotes4AllScreen_TestCase(ScreenTestCase):

    screenName = "quotes4all"
            
    def test_delay(self):
        screen = self.getScreen()
        self.assertEqual(screen.sleep_between_items, 10)
        targs = ['-d', '1']
        screen = self.getScreen(targs)
        self.assertEqual(screen.sleep_between_items, 1)

class MatrixScreen_TestCase(ScreenTestCase):
    screenName = "matrix"
    
    def test_kana(self):
        screen = self.getScreen()
        self.assertEqual(screen.use_kana_only, False)
        screen = self.getScreen(['-k'])
        self.assertEqual(screen.use_kana_only, True)
    
    def test_zenkaku(self):
        screen = self.getScreen()
        self.assertEqual(screen.use_zenkaku, False)
        screen = self.getScreen(['-z'])
        self.assertEqual(screen.use_zenkaku, True)
        
    def test_delay(self):
        screen = self.getScreen()
        self.assertEqual(screen.line_delay, 30 * constants.Settings.CHAR_DELAY_SECONDS)
        screen = self.getScreen(['-d', '1'])
        self.assertEqual(screen.line_delay, 1)

    def test_granularity(self):
        screen = self.getScreen()
        self.assertEqual(screen.granularity, 10)
        screen = self.getScreen(['-g', '2'])
        self.assertEqual(screen.granularity, 2)
    
    def test_all(self):
        screen = self.getScreen()
        self.assertEqual(screen.use_kana_only, False)
        self.assertEqual(screen.use_zenkaku, False)
        self.assertEqual(screen.line_delay, 30 * constants.Settings.CHAR_DELAY_SECONDS)
        self.assertEqual(screen.granularity, 10)
        screen = self.getScreen(['-k', '-d','1','-g', '2'])
        self.assertEqual(screen.use_kana_only, True)
        self.assertEqual(screen.use_zenkaku, False)
        self.assertEqual(screen.line_delay, 1)
        self.assertEqual(screen.granularity, 2)

class ProgrammerScreen_TestCase(ScreenTestCase):
    screenName = "programmer"
    
    required_args = ['-p', './empty-for-tests']
    
    def test_path(self):
        with self.assertRaises(SystemExit):
            self.getScreen()
        with self.assertRaises(PathNotFoundException):
            self.getScreen(['-p', './nonexistant-directory'])
        try:
            self.getScreen(self.required_args)
        except PathNotFoundException:
            self.fail("Testing for valid pathing failed.")

class RandTxtScreen_TestCase(ScreenTestCase):
    screenName = "randtxt"
    
    def test_word(self):
        screen = self.getScreen()
        self.assertEqual(screen.word, constants.App.TITLE)
        screen = self.getScreen(['-w', 'unittest'])
        self.assertEqual(screen.word, 'unittest')

    def test_delay(self):
        screen = self.getScreen()
        self.assertEqual(screen.freeze_delay, screen.FREEZE_WORD_DELAY)
        screen = self.getScreen(['-d', '1'])
        self.assertEqual(screen.freeze_delay, 1)
    
    def test_all(self):
        screen = self.getScreen()
        self.assertEqual(screen.word, constants.App.TITLE)
        self.assertEqual(screen.freeze_delay, screen.FREEZE_WORD_DELAY)
        screen = self.getScreen(['-w','unittest_all', '-d', '2'])
        self.assertEqual(screen.word, 'unittest_all')
        self.assertEqual(screen.freeze_delay, 2)

class RSSFeedScreen_TestCase(ScreenTestCase):
    screenName = 'rssfeed'

    required_args = ['-u', 'http://www.google.com/']
    
    def test_url(self):
        with self.assertRaises(InvalidOptionException):
            self.getScreen()
        try:
            self.getScreen(self.required_args)
        except InvalidOptionException:
            self.fail("Testing for valid url failed.")
    
    def test_raw(self):
        screen = self.getScreen(self.required_args)
        self.assertEqual(screen.clean_html, True)
        targs = self.required_args.copy()
        targs.extend(['-r'])
        screen = self.getScreen(targs)
        self.assertEqual(screen.clean_html, False)

class SysmonScreen_TestCase(ScreenTestCase):
    screenName = 'sysmon'

    def test_delay(self):
        screen = self.getScreen()
        self.assertEqual(screen.delay, 0.5)
        targs = ['-d', '5']
        screen = self.getScreen(targs)
        self.assertEqual(screen.delay, 5)
    
    def test_adjust(self):
        screen = self.getScreen()
        self.assertEqual(screen.adjust, True)
        targs = ['-n']
        screen = self.getScreen(targs)
        self.assertEqual(screen.adjust, False)
    
    def test_path(self):
        with self.assertRaises(PathNotFoundException):
            self.getScreen(['-p', './nonexistant-directory/invalidfile.txt'])
        try:
            self.getScreen(['-p', './empty-for-tests/testfile.txt'])
        except PathNotFoundException:
            self.fail("Testing for valid pathing failed.")

def run_tests():
    run_classes = [
        ClockScreen_TestCase,
        Img2AsciiScreen_TestCase,
        Jokes4AllScreen_TestCase,
        Quotes4AllScreen_TestCase,
        MatrixScreen_TestCase,
        ProgrammerScreen_TestCase,
        RandTxtScreen_TestCase,
        RSSFeedScreen_TestCase,
        SysmonScreen_TestCase
    ]
    
    loader = unittest.TestLoader()
    runner = unittest.TextTestRunner(buffer=None)
    
    simple_suites_list = []
    suites_list = []
    for test_class in run_classes:
        suite = loader.loadTestsFromTestCase(test_class)
        results = runner.run(suite)
        suites_list.append(
            {"name":test_class.__name__, "results":results}
        )
    for suite in suites_list:
        print(
            "%s - %s tests run. %s errors, %s failures" % 
            (
                suite['name'],
                str(suite['results'].testsRun),
                str(len(suite['results'].errors)),
                str(len(suite['results'].failures))
            )
        )
    
    # Just in case I want to do a big run.
    # for test_class in run_classes:
    #     suite = loader.loadTestsFromTestCase(test_class)
    #     simple_suites_list.append(suite)

    # combined_suite = unittest.TestSuite(simple_suites_list)
    # combined_runner = unittest.TextTestRunner()
    # combined_results = combined_runner.run(combined_suite)
    # print(combined_results)

if __name__ == "__main__":
    run_tests()