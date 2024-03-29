###############################################################################
#
# file:     __init__.py
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
"""
This module holds base classes that are used by all screens within termsaver
application. Each individual "screen" represents a unique screensaver that can
be triggered by termsaver.

The base classes available in this package are:

  * `ScreenBase`: the most basic screen class, which will handle simple
                  interaction with the terminal.

  * `filereader.FileReaderBase`: handles screens that require recursive
     directory scanning for files to be printed out

  * `urlfetcher.UrlFetcherBase`: handles screens that require Internet
     connectivity.

  * `urlfetcher.SimpleUrlFetcherBase`: similar as `UrlFetcherBase`,
     with simpler options (to avoid overhead to build your own argument
     parsing, and usage documentation)

  * `rssfeed.RSSFeedScreenBase`: handles RSS parsing from Internet.

  * `rssfeed.SimpleRSSFeedScreenBase`: similar as `RSSFeedScreenBase`,
     with simpler options (to avoid overhead to build your own argument
     parsing, and usage documentation)


Build your own screen
=====================

It is very simple to inherit from these base classes and create your own
screen. See some of the examples implemented here already. Basically, you will
need to:

    * define a name and description for your screen (class instantiation)
      and keep them as short as possible (avoid too much typing)

    * if applicable, define your command-line usage guidelines and options
      (see `cli_opts`), if appropriate and override `_parse_args` method.
      Create your help/usage text by overriding the `_usage_options_example`
      method.

    * build your action by overriding the `_run_cycle` method, if applicable
      (the base class will be triggered by the `autorun` method that loops
      indefinitely or until there is a keyboard interruption (ctrl+C).

Before you start, though, I strongly advise you to check out the code here
thoroughly, to avoid reinventing the wheel in parts that are already covered.
Additionally, consistency is important, so try to keep the same concept of how
things are done here... Well, if you have better idea, I am very opened to
adapt (but then instead of making a mess, we would change it all to be still
consistent).

"""

#
# Python built-in modules
#
import subprocess
import sys

from termsaver.termsaverlib.helper.utilities import show_stdout_cursor

pynput_installed = None
reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
if 'pynput' in installed_packages:
    pynput_installed = True
    from pynput import keyboard

#
# Internal modules
#
from termsaver.termsaverlib import constants
from termsaver.termsaverlib.i18n import _
from termsaver.termsaverlib.screen.helper import ScreenHelperBase


class ScreenBase(ScreenHelperBase):
    """
    This is the main screen that all screens must inherit in order to be part
    of the screensaver list, accessible with termsaver command-line options.

    When inheriting this to your own screen, remember to override the
    following methods:

        * `_run_cycle`: define here the algorithm to display a text-based
           look-alike screensaver. See other classes for example on how to
           use this.

        * `_usage_options_example`: print out here the options and examples
           on how to use your screen. See other classes for examples on how
           to use this.

        * `_parse_args`: from a properly parsed (using getopt) argument list,
           customize the configuration of your screen accordingly

    That's all you need to do!

    Additionally, you can also call the following helper methods:

        * `screen_exit`: if by any reason you need to close the application
          (remember, in most cases, you can just rely on throwing exceptions
          that are understood by termsaver application, available in
          `termsaverlib.exception` module)

        * `log` : if you need to write anything on screen before or after a
           screen cycle, you can do it in style by calling this method, which
           will inform the screen as a prefix to the message being displayed
           on screen.

    You can also use the following optional property:

        * `cleanup_per_cycle`:  Defines if the screen should be cleaned up for
           every rotation cycle (new file).

    IMPORTANT:
               All other methods are not to be tempered with!
    """

    name = ''
    """
    Defines the name of the screen.
    """

    parser = None
    """
    The argument parser for the screen
    """

    description = ''
    """
    Defines the description (short) of the screen.
    """

    cleanup_per_cycle = False
    """
    Defines if the screen should be cleaned up for every rotation cycle
    (new file).
    """

    def __init__(self, name, description, parser=None):
        """
        The basic constructor of this class. You need to inform basic
        information about your screen:

           * `name`: describes the name of the screen (try to keep it short,
                     and/or abbreviated, as much as possible)

           * `description`: a brief (very brief) description of what the screen
                            does (if you need to write more documentation about
                            it, you can rely on man docs for that)
        """
        self.parser = parser
        if self.parser:
            self.parser.prog = "termsaver " + name

        self.name = name
        self.description = description
        
        if pynput_installed is not None:
            self.listener = keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release
            )
    
    def on_press(self, key):
        """
        This method is called when a key is pressed.
        """
        if pynput_installed is not None:
            self.listener.stop()
    
    def on_release(self, key):
        """
        This method is called when a key is released.
        Unused for now, but leaving it in so we have options in the future.
        """
        pass

    def autorun(self, loop=True):
        """
        The accessible method for dynamically running a screen.
        This method will basically parse the arguments, prepare them with
        the method `_parse_args` that is inherited in sub-classes, and with
        the property `cli_opts` that holds the formatting of the arguments.

        Once all is ready to go, this will call the `_run_cycle` method, which
        is filled in the sub-classes with the algorithms to display text on
        screen to behave as a screensaver.

        The arguments of this method are:

            * args: (MANDATORY) the arguments passed when termsaver is executed
                    from command-line. See `termsaver` script for details.

            * loop: (OPTIONAL) defines if termsaver should be executing on an
                    infinite looping (goes on until the keyboard interrupt
                    (Ctrl+C) is pressed), or not. This is up to the screen
                    action (or end-user through configuable setting) to decide.
        """
        # execute the cycle
        self.clear_screen()

        if pynput_installed is not None:
            self.listener.start()
        while(
            (loop and pynput_installed is None)
            or
            (loop and pynput_installed is not None and self.listener.is_alive())
        ):
            try:
                self._run_cycle()
            except KeyboardInterrupt as e:
                #
                # do some cleanup if applicable
                #
                self._on_keyboard_interrupt()
                raise e

            # Clear screen if appropriate
            if self.cleanup_per_cycle:
                self.clear_screen()
        show_stdout_cursor()

    def _run_cycle(self):
        """
        Executes a cycle of this screen. This base class actually does not hold
        any special actions to begin with, but executing it from inheriting
        classes is also a good practice, to allow future implementations that
        must be taken from a base class.
        """
        pass

    @staticmethod
    def usage_header():
        """
        Simply prints a header information, used with the `usage` method.

        See also `usage` method for details.
        """
        print ("""%(app_title)s v.%(app_version)s - %(app_description)s.
""" % {
               'app_title': constants.App.TITLE,
               'app_version': constants.App.VERSION,
               'app_description': constants.App.DESCRIPTION,
        })

    @staticmethod
    def usage_footer():
        """
        Simply prints a footer information, used with the `usage` method.

        See also `usage` method for details.
        """
        print ("""--
See more information about this project at:
%(url)s

Report bugs to authors at:
%(source_url)s
""" % {
        'url': constants.App.URL,
        'source_url': constants.App.SOURCE_URL,
       })

    def _usage_options_example(self):
        """
        Describe here the examples of your screen.
        See some examples of already implemented base screens so you can
        write similar stuff on your own, and keep consistency.
        """
        pass

    def usage(self):
        """
        Defines the usage information that is presented when a user hits the
        help option.You should not directly override this method, instead, just
        override the protected method `_usage_options_example`, created for
        this purpose. All other stuff will be defined by the `usage_header` and
        `usage_footer` methods.
        """

        # header
        self.usage_header()

        print (_("""Screen: %(screen)s
Description: %(description)s""") % {
               'app_name': constants.App.NAME,
               'screen': self.name,
               'description': self.description,
        })
        # any additional info in between (see other classes for reference)
        if self.parser:
            self.parser.print_help()

        usage = self._usage_options_example()
        if usage != None and usage != '':
            print(_("\r\nExamples:"))
            print(usage)

        #footer
        self.usage_footer()

    def _parse_args(self, launchScreenImmediately=True):
        """
        (protected) MUST be overriden in inheriting classes, to deal with
        special arguments that will customize values for them.
        """
        pass

    def screen_exit(self, error=0):
        """
        Exits the screen (and finishes the application) with a specific error.
        If none is informed, it exits as successful (error 0).
        """
        sys.exit(error)

    def log(self, text):
        """
        Prints a log message on screen in the format:
            %(app_name)s.%(screen)s: %(message)s
        """
        print ("%s.%s: %s" % (constants.App.NAME, self.name, text))

    def _on_keyboard_interrupt(self):
        """
        Executes extra commands if the keyboard interrupt exception happened
        while running a cycle. 
        """
        pass