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
The HTML render/parser program.
"""

OUTPUT = '/tmp/readme.html'
"""
The temporary location for the HTML rendered file based on the README.
"""

README = 'README.md'
"""
The location of the readme markdown file.
"""

def usage():

    print """Usage: %(program)s [OPTIONS]

This script will automatically output the HTML of the markdown of the README
file, and open it on the system default browser, for convenience.

Options:

 -h, --help      displays this help message
 -m, --monitor   automatically update the HTML rendering file whenever 
                 the README file is modified (it will not trigger the browser)
 -f file, --file=file 
                 the file to be monitored and parsed. If none informed, it will
                 use %(file)s
 -p program, --program=program   
                 the program used for rendering the file into a HTML format
                 If none informed, it uses markdown.
                 
Examples:

%(program)s -m -f README.md -p markdown
This will generate a HTML view of the Markdown syntax, used by GitHub.

%(program)s -m -f extras/README.dist -p rst2html
This will generate a HTML view of the Restructured Text syntax, 
used by Python PyPi.

""" % {'program': os.path.basename(__file__)}


def render(program, readme, output):
    chk_program(program)
    if os.system("%s %s > %s" % (program, readme, output)) != 0:
        raise Exception("Unable to properly execute rendering.")


def chk_program(program):
    if os.system("which %s >/dev/null" % program) != 0:
        print """%(script)s script requires %(program)s program. 
In Ubuntu, you can simply install it by executing: 
        sudo apt-get install %(program)s""" % {
            'script': os.path.basename(__file__), 
            'program': program
        }
        sys.exit(2)    
    
def trigger_browser(output):
    if os.system("xdg-open %s &" % output) != 0:
        raise Exception("Unable to properly open default browser.")


def sha1sum(readme):
    f = open(readme, "rb")
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

    global PROGRAM, README, OUTPUT
    
    monitor = False
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hmf:p:", 
            ["program=", "file=", "help", "monitor"])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) 
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
        elif o in ("-f", "--file"):
            README = a
            if not os.path.exists(README):
                raise Exception("File %s does not exist!" % a)
        elif o in ("-p", "--program"):
            PROGRAM = a
            chk_program(a)
        else:
            assert False, "unhandled option"    

    if monitor:
        print "Running a monitor at file [%s] for program [%s]..." % \
            (README, PROGRAM)
        sumhash = ''
        while True:
            if sumhash != sha1sum(README):
                echo("Detected change. updating HTML file...\n")
                render(PROGRAM, README, OUTPUT)
                sumhash = sha1sum(README)
            else:
                echo("monitoring [%s]...")  
                time.sleep(1)      
    else:
        render(PROGRAM, README, OUTPUT)
        trigger_browser(OUTPUT)


if __name__ == "__main__":
    main()

