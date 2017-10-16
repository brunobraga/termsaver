# -*- coding: utf-8 -*-
###############################################################################
#
# file:     sysmon.py
#
# Purpose:  refer to python doc for documentation details.
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
This module contains a simple screen that displays CPU/MEM charts.
See additional information in the class itself.

The screen class available here is:

    * `SysmonScreen`
"""

#
# Python mobdules
#
import time
import re
import os

#
# Internal modules
#
from termsaverlib.screen.base import ScreenBase
from termsaverlib.screen.helper.position import PositionHelperBase
from termsaverlib import constants, exception, common
from termsaverlib.i18n import _


class SysmonScreen(ScreenBase, PositionHelperBase):
    """
    Simple screen that displays CPU/MEM usage charts on a terminal window.

    From its base classes, the functionality provided here bases on the
    settings defined below:

        * clean up each cycle: False
          The screen will be cleared manually after the CPU calculation
          is completed (it requires a sleep)

    """

    path = None
    """
    Defines the path of the file containing a monitoring value, from 0 to 100.
    """

    info = {
            'db': [
                #
                # store data in format: 
                # {'time': ??, 'cpu': ??, 'mem': ??, 'extra': ??}
                #
            ],
            'total_mem': 0,
            'max_cpu': 0,
            'max_mem': 0,
            'max_extra': 0, # for an external path
    }
    """
    Registers the history of CPU/MEM usage, used to build the charts
    """

    delay = None
    """
    Defines the printing delay, to give a cool visual of a
    moving screen. This value is measured in seconds, and default is 0.5.
    """


    #
    # Graphical elements
    #

    pie_chart = ['○', '◔', '◑', '◕', '●']
    """
    Holds the unicode symbols for pie chart representation of percentage
    """
    block = [' ', '▁', '▂', '▃', '▄', '▅', '▆', '▇', '█', '█']
    """
    Holds the block unicode symbolds used to draw the charts
    """
    axis_corner = "└"
    """
    Represents the unicode symbol for the axis corner in the xy chart
    """
    axis_h = "─"
    """
    Represents the unicode symbol for the horizontal axis in the xy chart
    """
    axis_v = "│"
    """
    Represents the unicode symbol for the vertical axis in the xy chart
    """

    adjust = True
    """
    Defines if the graphics should hold a 0-100 count or adjust to the highest
    value available
    """


    def __init__(self):
        """
        The constructor of this class.
        """
        ScreenBase.__init__(self,
            "sysmon",
            _("displays a graphical system monitor"),
            {'opts': 'hd:np:', 'long_opts': ['help', 'delay=', 'no-adjust', 'path=']},
        )
        if self.delay is None:
            self.delay = 0.5

        #
        # Due to a time delay to calculate CPU usage
        # we need to clear the screen manually
        #
        self.cleanup_per_cycle = False


    def _run_cycle(self):
        """
        Executes a cycle of this screen.
        """

        # calculate random position based on screen size
        self.get_terminal_size()

        # update info data
        if self.path:
            #
            # run the flow for external path
            #
            self.update_stats_extra()
            
            if self.geometry['x'] > 16: # just to avoid unexpected exceptions
                title = "%s: %s" % (_('Monitoring'), (self.path[:(self.geometry['x'] - 16)] 
                        + (self.path[(self.geometry['x'] - 16):] and '...')))
            else:
                title = _("Monitoring file")
                
            txt = self.get_xy_chart(title, 'extra')
            
            txt += self.center_text_horizontally(
                "\n  Load: %s%%   %s " % (
                ("%02d" % self.info['db'][-1]['extra']),
                self.get_chart(self.info['db'][-1]['extra']),
                )
            ) 
            
        else:
            #
            # run the flow for CPU/Mem as default
            #
            self.update_stats()

            txt = self.get_xy_chart("CPU Monitor", 'cpu')
    
            txt += "\n"
    
            txt += self.get_xy_chart("MEM Monitor", 'mem')
    
            txt += self.center_text_horizontally(
                "\n%s  CPU: %s%%   %s  MEM: %s%% (total %sMB)" % (
                self.get_chart(self.info['db'][-1]['cpu']),
                ('%.1f' % self.info['db'][-1]['cpu']),
                self.get_chart(self.info['db'][-1]['mem']),
                self.info['db'][-1]['mem'],
                int(self.info['total_mem'])
            ))

        #
        # Due to a time delay to calculate CPU usage
        # we need to clear the screen manually
        #
        self.clear_screen()

        # just print the whole text
        print txt

        #
        # The sleep happens here in the CPU calculation instead
        #
        #time.sleep(self.delay)

    def update_stats_extra(self):
        """
        Updates the info property with latest information on an extra path, 
        defined by --path argument option

        Note: This also takes care of sleep (defined by delay property)
        """
        
        f = open(self.path, 'r')
        try:
            val = int(f.read())
        except:
            raise exception.TermSaverException(
               _('The file does not contain an integer as expected.'))
        if val < 0 or val > 100:
            raise exception.TermSaverException(
                _('The file contains invalid data (must be between 0 and 100).'))
        f.close()

        # cut the data to keep only recent values
        self.info['db'] = self.info['db'][-(self.geometry['x'] - 5):]

        max_extra = 0
        for item in self.info['db']:
            if item['extra'] > max_extra:
                max_extra = item['extra']
        self.info['max_extra'] = max_extra
        self.info['db'].append( {
                'time': time.time(),
                'extra': val,
             }
        )
        time.sleep(self.delay)
        
        
    def update_stats(self):
        """
        Updates the info property with latest information on CPU and MEM usage.

        Note: This also takes care of sleep (defined by delay property)
        """
        
        # TODO - Implement similar features for Windows/Mac OS
        #        maybe consider psutil package
        if os.name != "posix":
            raise exception.TermSaverException(help_msg="OS is not supported!")

        # memory info
        mem_info = common.get_mem_usage()
        
        # cpu info
        cpu = common.get_cpu_usage(self.delay)

        self.info['total_mem'] = mem_info[1]

        # insert into history data
        self.info['db'].append( {
                'time': time.time(),
                'cpu': cpu,
                'mem': mem_info[0]
             }
        )
        # cut the data to keep only recent values
        self.info['db'] = self.info['db'][-(self.geometry['x'] - 5):]

        # recalculate the cpu ceiling value
        max_cpu, max_mem = 0, 0
        for item in self.info['db']:
            if item['cpu'] > max_cpu:
                max_cpu = item['cpu']
            if item['mem'] > max_mem:
                max_mem = item['mem']
        self.info['max_cpu'] = max_cpu
        self.info['max_mem'] = max_mem


    def format_time(self, epoch):
        """
        Formats a given epoch time into a very simplistic form compared to
        current time (eg. 1h meaning 1 hour ago).
        """
        elapsed = time.time() - epoch
        if elapsed > 3600:
            return "%.1fh" % (elapsed/3600.0)
        elif elapsed > 60:
            return "%.1fm" % (elapsed/60.0)
        elif elapsed > 1:
            return "%.1fs" % elapsed
        else:
            return ""

    def get_chart(self, perc):
        """
        returns a pie chart unicode depending on the percentage (eg. 100%)
        given.
        """
        pos = int(perc * 5 / 100)
        if pos < len(self.pie_chart) and pos >= 0:
            return self.pie_chart[pos]
        else:
            return ""

    def get_xy_chart(self, title, key):

        ceiling = 100
        if self.adjust:
            ceiling = self.info['max_' + key]

        ysize = int((self.geometry['y'] - 13)/2) # remove lines used
        current_position = 0

        txt = self.align_text_right(title) + "\n" \
            + ('%.0f' % ceiling) + "%\n"
        # create output (11 lines)
        for y in range(ysize - 1, -1, -1):
            current_position = 0
            txt += " " + self.axis_v
            for x in range(self.geometry['x'] - 5): # padding
                if len(self.info['db']) - 1 < x:
                    txt += " "
                else:
                    current_position += 1

                    # to keep proportions
                    ratio = 1
                    if ceiling > 0:
                        ratio = int(self.info['db'][x][key] * ysize / ceiling)

                    # based on number of blocks (10)
                    if ratio >= y + 1:
                        txt += self.block[-1]
                    elif y > 0 and ratio > y:
                        txt += self.block[ratio - y]
                    elif y > 0:
                        txt += self.block[0]
                    else:
                        txt += self.block[1]

            txt += "\n"

        txt += " " + self.axis_corner + self.axis_h * (self.geometry['x'] - 5) + "\n"

        txt += "%s%s%s\n" % (self.format_time(self.info['db'][0]['time']),
                " " * (current_position - 5), _("now"))

        return txt

    def _usage_options_example(self):
        """
        Describe here the options and examples of this screen.

        The method `_parse_args` will be handling the parsing of the options
        documented here.

        Additionally, this is dependent on the values exposed in `cli_opts`,
        passed to this class during its instantiation. Only values properly
        configured there will be accepted here.
        """
        print _("""
Options:

 -d, --delay  Sets the speed of the displaying characters
              default is 0.5 seconds (advised to keep at least above 0.1).
 -n, --no-adjust
              Forces the charts to displays 0 ~ 100%% values, instead of
              dynamically adjusted values based on current maximum.
 -p, --path   Sets the location of a file to be monitored. The file must only
              contain a number from 0 to 100, or the screen will not start.
              This option is optional.               
 -h, --help   Displays this help message

Example:

    $ %(app_name)s %(screen)s
    This will trigger the screensaver to display a dot on screen, with random
    size increase.

    $ %(app_name)s %(screen)s -d 5
    Overrides the default delay to 5 seconds

""") % {
        'app_name': constants.App.NAME,
        'screen': self.name,
       }

    def _parse_args(self, prepared_args):
        """
        Handles the special command-line arguments available for this screen.
        Although this is a base screen, having these options prepared here
        can save coding for screens that will not change the default options.

        See `_usage_options_example` method for documentation on each of the
        options being parsed here.

        Additionally, this is dependent on the values exposed in `cli_opts`,
        passed to this class during its instantiation. Only values properly
        configured there will be accepted here.
        """
        for o, a in prepared_args[0]:  # optlist, args
            if o in ("-h", "--help"):
                self.usage()
                self.screen_exit()
            elif o in ("-n", "--no-adjust"):
                self.adjust = False
            elif o in ("-p", "--path"):
                # make sure argument is a valid value (existing path)
                self.path = a
                if not os.path.exists(self.path):
                    raise exception.PathNotFoundException(self.path,
                        _("Make sure the file exists."))
                if not os.path.isfile(self.path):
                    raise exception.InvalidOptionException("--path",
                        _("Make sure it is a file"))
                    
            elif o in ("-d", "--delay"):
                try:
                    # make sure argument is a valid value (float)
                    self.delay = float(a)
                except:
                    raise exception.InvalidOptionException("delay")
            else:
                # this should never happen!
                raise Exception(_("Unhandled option. See --help for details."))
