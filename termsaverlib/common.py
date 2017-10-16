###############################################################################
#
# file:     common.py
#
# Purpose:  holds common helper functions used by termsaver code.
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
Holds common functionality used by termsaver screens.
"""

#
# Python build-in modules
#
import os
import sys
import traceback
import HTMLParser
import subprocess
import re
import time


def is_windows():
    """
    Returns True if the environment is Microsoft Windows.
    """
    return sys.platform == "win32"


def is_macos():
    """
    Returns True if the environment is Microsoft Windows.
    """
    return sys.platform == "darwin"


def prettify_exception(ex):
    """
    Outputs the exception with its stack trace within separator lines.
    """
    print """
===================================
Exception: (%s) %s
%s
===================================
""" % (ex.__class__.__name__, ex.message, traceback.format_exc())


def get_app_dir():
    """
    Retrieves the termsaver main directory based on current operating system.

    For Windows machines, this should be something like:

        <root>\Documents and Settings\<user>\Application Data\termsaver

    For Unix machines, it will be:

        /home/<user>/.termsaver/
    """
    if is_windows():
        path = os.path.join(os.environ['APPDATA'], "termsaver")
    else:
        path = os.path.join(os.environ['HOME'], ".termsaver")

    # create if applicable
    if not os.path.exists(path):
        # permission errors here will just propagate error
        os.mkdir(path)

    return path


def get_temp_dir():
    """
    Retrieves the temporary based on current operating system.

    For Windows machines, this should be something like:

        <root>\Documents and Settings\<user>\Local Settings\Temp

    For Unix machines, it will be:

        /tmp/

    """
    if is_windows():
        path = os.environ['TMP']
    else:
        path = "/tmp"

    return path


def unescape_string(escaped_text):
    """
    Unescape strings. This is useful for cases when data that needs to be
    displayed on screen is escaped for HTML or database stuff.

    Additional replacing is taken here, such as some HTML tags:

        * <br>, replaced to \n
    """
    unescaped = escaped_text
    try:
        unescaped = HTMLParser.HTMLParser().unescape(escaped_text)
        # replace most common HTML data
        unescaped = unescaped.replace('<br>', '\n')
        unescaped = unescaped.replace('<br/>', '\n')
        unescaped = unescaped.replace('<br />', '\n')
        unescaped = unescaped.decode('string_escape')
    except:
        #
        # If there were errors here, just ignore them and try to give back
        # the string the best it could do
        #
        pass
    return unescaped


def get_day_suffix(day):
    """
    Returns the suffix of the day, such as in 1st, 2nd, ...
    """
    if day in (1, 21, 31):
        return 'st'
    elif day in (2, 12, 22):
        return 'nd'
    elif day in (3, 23):
        return 'rd'
    else:
        return 'th'


def execute_shell(cmd, ignore_errors=False):
    """
    Simple routine to execute shell commands.
    If `ignore_errors` is false (default) errors here will be thrown, and
    must be treated individually, to ensure proper message to end-user.

    The `cmd` argument must be an array, formatted for subprocess.Popen.
    If you are not sure on how to do that, just use:  shlex.split(string).
    """
    try:
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                stdout=subprocess.PIPE, close_fds=True)
        out, __ = p.communicate()
    except Exception, e:
        if not ignore_errors:
            raise e
    return out.rstrip()


def strip_html(text):
    """
    Simple regex that cleans a string of any HTML tags (for terminal output,
    there isn't much sense to have them printed anyway).
    """
    return re.sub('<[^<]+?>', '', text)


def get_cpu_usage(sleep_delay, ignore_errors=False):
    """
    """
    try:    
        if is_windows():
            raise Exception(_("Functionality not available for Windows. See --help for details."))
            
        elif is_macos():
            ps = subprocess.Popen(['ps', '-A', '-o %cpu'], stdout=subprocess.PIPE)
            cpu = subprocess.check_output(('awk', '{s+=$1} END {print s "%"}'), stdin=ps.stdout)
            ps.wait()
            time.sleep(sleep_delay) # required to simulate same in linux
            return float(cpu.strip()[:-1])

        else:
            # linux
            def getTimeList():
                statFile = file("/proc/stat", "r")
                timeList = statFile.readline().split(" ")[2:6]
                statFile.close()
                for i in range(len(timeList))  :
                    timeList[i] = int(timeList[i])
                return timeList
            def deltaTime()  :
                x = getTimeList()
                time.sleep(sleep_delay)
                y = getTimeList()
                for i in range(len(x))  :
                    y[i] -= x[i]
                return y
            dt = deltaTime()
            if sum(dt) > 0:
                cpu = 100 - (dt[len(dt) - 1] * 100.00 / sum(dt))
            else:
                cpu = 0

            return cpu

    except Exception, e:
        if not ignore_errors:
            raise e
        else:
            return 0


def get_mem_usage(ignore_errors=False):
    """
    """
    try:    
        if is_windows():
            raise Exception(_("Functionality not available for Windows. See --help for details."))
            
        elif is_macos():

            vm = subprocess.Popen(['vm_stat'], stdout=subprocess.PIPE).communicate()[0].decode()
            vmLines = vm.split('\n')
            sep = re.compile(':[\s]+')
            vmStats = {}
            for row in range(1,len(vmLines)-2):
                rowText = vmLines[row].strip()
                rowElements = sep.split(rowText)
                vmStats[(rowElements[0])] = int(rowElements[1].strip('\.')) * 4096

            total_mem = (vmStats["Pages wired down"]+vmStats["Pages active"]+vmStats["Pages inactive"]+vmStats["Pages free"])/1024/1024
            curr_mem = (vmStats["Pages inactive"]+vmStats["Pages free"]) * 100 / (vmStats["Pages wired down"]+vmStats["Pages active"]+vmStats["Pages inactive"]+vmStats["Pages free"])

            return (curr_mem, total_mem)

        else:
            # linux
            re_parser = re.compile(r'^(?P<key>\S*):\s*(?P<value>\d*)\s*kB')
            mem_info = {}
            for line in open('/proc/meminfo'):
                match = re_parser.match(line)
                if not match:
                    continue # skip lines that don't parse
                key, value = match.groups(['key', 'value'])
                if key not in ('MemTotal', 'MemFree'):
                    continue
                mem_info[key] = int(value)

            total_mem = mem_info['MemTotal'] / 1024
            curr_mem = (mem_info['MemTotal'] - mem_info['MemFree']) * 100 / mem_info['MemTotal']

            return (curr_mem, total_mem)

    except Exception, e:
        if not ignore_errors:
            raise e
        else:
            return (0,0)




