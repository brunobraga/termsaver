###############################################################################
#
# file:     position.py
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
A helper class that provides positioning functionality to screens, such as
defining a terminal size, and centering information (horizontally or
vertically).

See additional information in the class itself.

The helper class available here is:

    * `PositionHelperBase`

"""
#
# Python built-in modules
#
import sys
import time
import platform
import math
import random

#
# Internal modules
#
from termsaverlib.screen.helper import ScreenHelperBase


class PositionHelperBase(ScreenHelperBase):
    """
    This helper class provides positioning functionality to the screens,
    by dealing with the current dimensions of the terminal.

    There are main methods available here:

        * `get_terminal_size`: retrieves the current terminal dimensions, width
           and height, to be stored in local properties `screen_width` and
           `screen_height`.

        * `center_text_vertically`: centers a specified text in vertical

        * `center_text_horizontally`: centers a specified text in horizontal

        * `randomize_text_vertically`: randomizes a specified text in vertical

        * `randomize_text_horizontally`: randomizes a specified text in 
           horizontal

    If the method `get_terminal_size` is never called, all other functionality,
    relying on terminal dimensions, will just based on a default size, set as
    80x25.
    """

    screen_width = 80
    """
    Defines the current terminal width. Its default value is set as 80.
    """

    screen_height = 25
    """
    Defines the current terminal height. Its default value is set as 25.
    """
    
    pos_y = 1
    """
    Stores the latest position Y axis (height) position value after calling
    the randomizing methods of this class (useful to allow you to know the
    previous location of the text in the window) 
    """

    pos_x = 1
    """
    Stores the latest position X axis (width) position value after calling
    the randomizing methods of this class (useful to allow you to know the
    previous location of the text in the window) 
    """
    
    def center_text_vertically(self, text):
        """
        Returns the text argument with additional new lines, calculated to
        display the text in the vertical center of the screen.

        Arguments:

            * text: the text to be vertically centered
        """
        line_count = 0
        for t in text.split("\n"):
            line_count += 1 + math.ceil(len(t) / (self.screen_width - 1))
    
        return "\n" * int(math.floor((self.screen_height - line_count) / 2)) \
            + text
    
    
    def center_text_horizontally(self, text):
        """
        Returns the text argument with additional blank spaces, calculated to
        display the text in the horizontal center of the screen.

        Arguments:

            * text: the text to be horizontally centered
        """
        new_text = ""
        for t in text.split("\n"):
            temp = [""]
            index = 0
            for w in t.split(" "):
                if len(temp[index] + w) < self.screen_width - 1:
                    temp[index] = " ".join([temp[index], w])
                else:
                    index += 1
                    temp.append(w)
            for l in temp:
                new_text += " " * int(math.ceil(
                    (self.screen_width - len(l) - 1) / 2)) + l + "\n"
    
        return new_text

    def randomize_text_horizontally(self, text):
        """
        Returns the text argument with additional blank spaces, calculated to
        display the text in a random position of the screen.

        Arguments:

            * text: the text to be horizontally randomized
        """
        self.pos_x = random.randint(0, self.screen_width - len(text))

        return " " * self.pos_x + text \
            + " " * (self.screen_width - self.pos_x - len(text))

    def randomize_text_vertically(self, text):
        """
        Returns the text argument with additional new lines, calculated to
        display the text in a random position of the screen.

        Arguments:

            * text: the text to be vertically randomized
        """
        self.pos_y = random.randint(0, self.screen_height)
        
        return "\n" * self.pos_y + text

    def get_terminal_size(self):
        """ 
        Retrieves the screen terminal dimensions, returning a tuple
        (width, height), and will also store them in internal properties 
        `screen_width` and `screen_height`.
        
        Copyright note:
        This code has been adapted from:
        http://stackoverflow.com/questions/566746/\
            how-to-get-console-window-width-in-python

        posted by Harco Kuppens, at Jul 1 '11 at 16:23.

        """
        
        # This is required if you are programming from non-windows platforms
        # more on this at: http://pydev.org/manual_adv_assistants.html
        #@PydevCodeAnalysisIgnore
        def _get_terminal_size_windows():
            res = None
            try:
                from ctypes import windll, create_string_buffer
        
                # stdin handle is -10
                # stdout handle is -11
                # stderr handle is -12
                h = windll.kernel32.GetStdHandle(-12)
                csbi = create_string_buffer(22)
                res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
            except:
                return None
            if res:
                import struct
                (_, _, _, _, _,
                 left, top, right, bottom, _, _) = struct.unpack("hhhhHhhhhhh",
                                                                 csbi.raw)
                sizex = right - left + 1
                sizey = bottom - top + 1
                return sizex, sizey
            else:
                return None
        
        def _get_terminal_size_tput():
            try:
                import subprocess
                proc = subprocess.Popen(["tput", "cols"], 
                                        stdin = subprocess.PIPE, 
                                        stdout = subprocess.PIPE)
                output = proc.communicate(input = None)
                cols = int(output[0])
                proc = subprocess.Popen(["tput", "lines"], 
                                        stdin = subprocess.PIPE, 
                                        stdout = subprocess.PIPE)
                output = proc.communicate(input = None)
                rows = int(output[0])
                return (cols, rows)
            except:
                return None
        
        
        def _get_terminal_size_linux():
            def ioctl_GWINSZ(fd):
                try:
                    import fcntl, termios, struct
                    cr = struct.unpack('hh', fcntl.ioctl(fd, 
                                                         termios.TIOCGWINSZ, 
                                                         '1234'))
                except:
                    return None
                return cr
            cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
            if not cr:
                try:
                    fd = os.open(os.ctermid(), os.O_RDONLY)
                    cr = ioctl_GWINSZ(fd)
                    os.close(fd)
                except:
                    pass
            if not cr:
                try:
                    cr = (os.environ['LINES'], os.environ['COLUMNS'])
                except:
                    return None
            return int(cr[1]), int(cr[0])
        
        current_os = platform.system()
        tuple_xy = None
        if current_os == 'Windows':
            tuple_xy = _get_terminal_size_windows()
            if tuple_xy is None:
                tuple_xy = _get_terminal_size_tput()
                # needed for window's python in cygwin's xterm!
        if current_os == 'Linux' or current_os == 'Darwin' or \
                current_os.startswith('CYGWIN'):
            tuple_xy = _get_terminal_size_linux()
        if tuple_xy is None:
            tuple_xy = (80, 25)  # default value
        
        # assign result to 
        self.screen_width, self.screen_height = tuple_xy

        return tuple_xy
