#!/usr/bin/python
###############################################################################
#
# file:     readme_render.py
#
# Purpose:  simple script to render the markdown of the README file.
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
# Python modules
#
import os
import sys
import getopt
import hashlib
import datetime
import time


PROGRAM = 'markdown'
"""
The markdown parser program.
"""

OUTPUT = '/tmp/readme.markdown.html'
"""
The temporary location for the HTML rendered file based on the README markdown.
"""

README = '../README'
"""
The location of the readme markdown file.
"""

def usage():

    print """Usage: %s [options]

This script will automatically output the HTML of the markdown of the README
file, and open it on the system default browser, for convenience.

Options:

 -h, --help      displays this help message
 -m, --monitor   automatically update the HTML rendering file whenever 
                 the README file is modified (it will not trigger the browser)

""" % (os.path.basename(__file__))


def render():
    if os.system("which %s >/dev/null" % PROGRAM) != 0:
        print """%(script)s script requires %(program)s program. 
In Ubuntu, you can simply install it by executing: 
        sudo apt-get install %(program)s""" % {'script': os.path.basename(__file__), 
                                               'program': PROGRAM}
        sys.exit(2)

    os.system("%s %s > %s" % (PROGRAM, README, OUTPUT))
    
    
def trigger_browser():
    os.system("xdg-open %s &" % OUTPUT)


def sha1sum():
    f = open(README, "rb")
    h = hashlib.sha1()
    h.update(f.read())
    filehash = h.hexdigest()
    f.close()
    return filehash.lower()

def echo(text, new_line=False):
    sys.stdout.write("%s%s - %s" % (
        '' if new_line else '\r',
        datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        text))
    sys.stdout.flush()

def main():

    monitor = False
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hm", ["help", "monitor"])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    output = None
    verbose = False
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-m", "--monitor"):
            monitor = True
        else:
            assert False, "unhandled option"    

    if monitor:
        print "Running a monitor at [%s]..." % README
        sumhash = ''
        while True:
            if sumhash != sha1sum():
                echo("Detected change. updating HTML file...\n")
                render()
                sumhash = sha1sum()
            else:
                echo("monitoring [%s]...")  
                time.sleep(1)      
    else:
        render()
        trigger_browser()


if __name__ == "__main__":
    main()

