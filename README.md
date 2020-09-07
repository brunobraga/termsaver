<!-- 
###############################################################################
#
# file:     README.md
#
# Purpose:  holds basic information about termsaver application, 
#           in markdown format for GitHub.
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
-->

TermSaver
=========

*A simple text-based screensaver for terminal windows.*

You may also want to visit our website: 

**<http://termsaver.brunobraga.net>**

![termsaver](https://github.com/brunobraga/termsaver/raw/master/extras/termsaver-main_medium.jpeg)


Background
----------

The motivation behind this project is basically pure boredom (laughs). 
Seriously, it may look like nonsense to have a screensaver look-alike program
running on a terminal window. Nonetheless, sometimes, we still want to see some
kind of movement, or action on the screen... which invigorates one's state of
mind and helps concentration back to the black screen (well, some people like 
it white, meh!).

If you are:

  * looking for some extra display on your main terminal window, to keep the 
    screen busy while you are up to something else; or
  * looking for some distractions that may entertain you after too many hours
    in front of the terminal; or
  * with plenty of screen space (so long 80x25 default terminal window! long 
    live 1920px...), and use many terminals on screen; or
  * just wanting to pretend you are busy with something (this is terrible)

then, TermSaver is the **right** application for you.


Requirements
------------

  * Linux, or Mac (or Windows too, but you are on your own)
  * Python 3.x (Python 2.x was deprecated since 08-2020)


Installation
------------

#### Apt (Advanced Packaging Tool)

For Ubuntu (12.10+) distro, you can use:

        sudo apt-get install termsaver


#### Pip (Pip Installs Packages, for Python Package Index)

For those using others, and still want to do it the easy way, I recommend:

        sudo pip install termsaver


#### From the Source

For the brave (laughs), you can compile/install from the source:

1. Download the Source 
[here](http://pypi.python.org/pypi/termsaver/)
2. Unpack it
     
        tar -zxvf termsaver-{version}.tar.gz

3. Install it

        sudo python setup.py install 


#### PPA (Personal Package Archive)

If you can't wait for Debian/Ubuntu releases, you can get the latest packages from:

        sudo add-apt-repository ppa:bruno-braga/termsaver
        sudo apt-get update
        sudo apt-get install termsaver


Features
--------

The TermSaver is a very simple application, built with the idea to allow more 
screensavers to be added to its core. Developers, please read the section below. 

The current published screensavers are:


#### Ascii Art Farts

This is a screensaver that displays ascii art from asciiartfarts.com 
RSS feed in an animation format. 


#### Jokes For All

This is a screensaver that displays recent jokes from <http://jokes4all.net>
website, from its hourly updated [RSS](http://en.wikipedia.org/wiki/RSS) feed.


#### Programmer

This is a screensaver that displays source code from a specified path in
visual animation. If the [pygments](https://pygments.org/) package is installed, this screensaver
will use it to color the displayed files based on their type.

#### Quotes For All

This is a screensaver that displays recent quotes from <http://quotes4all.net>
website, from its hourly updated [RSS](http://en.wikipedia.org/wiki/RSS) feed.


#### Random Text

This is a screensaver that displays a text (your name, or whatever) on a 
 randomized position of the screen, changing position every N seconds.


#### Request for Comments

This is a screensaver that fetches documents from RFC (Request for Comments)
in visual animation, which are documents elaborated by the  Internet 
Engineering Task Force, available at <http://tools.ietf.org/rfc/>. This 
screensaver randomizes documents to display, from a list of latest valid
documents. See more information about this in 
[Wikipedia](http://en.wikipedia.org/wiki/Request_for_Comments).


#### RSS Feeds

This is a screensaver that displays any 
[RSS](http://en.wikipedia.org/wiki/RSS) feed you want to show in your
terminal, with customizable settings and format.


#### URL Fetcher

This is a screensaver that displays content from a specified 
[URL](http://en.wikipedia.org/wiki/Uniform_resource_locator) directly
on screen, in visual animation.


#### Clock

This is a screensaver that displays a digital clock using ascii letters.


#### Matrix

This is a screensaver that displays falling (rising) Japanese characters
simulating the screen from the movie 
[The Matrix](http://en.wikipedia.org/wiki/The_Matrix).


#### Sysmon

(For Linux/Mac systems only) Displays the CPU/Memory usage over time in a graphic
alike screensaver.


#### Star Wars Asciimation

This is a screensaver that displays the Star Wars Asciimation from
<http://asciimation.co.nz>.

 - - -

**Disclaimer Note**: termsaver holds no responsibility for the contents offered 
by third-parties, nor it has controls to filter them. Use it at your own risk.


Developers
----------

A more detailed guideline for developers willing to jump in and create 
screensavers for termsaver is here: <https://github.com/brunobraga/termsaver/wiki/Developers>


Roadmap
-------

There is no current roadmap defined, besides improvement tickets created in
[Issues](https://github.com/brunobraga/termsaver/issues) tab in GitHub.
Refer also to <http://github.com/brunobraga/termsaver/wiki/Brainstorming> for
some insights of stuff we are thinking about.

Contribute
----------

### Translation

The internationalization of this application follows same standards of most
applications out there, by using *gettext* and MO/PO files.

The translation is still being finished up, and when it is ready for 
contributor calls, we will post detailed information about the procedure.


### Screensavers (plugin)

As of v0.2, full plugin support is available, find an example here:

https://github.com/brunobraga/termsaver-figlet


### Submit a bug

If you find any errors in this application, you are more than welcome to 
participate. You can:

* report the bug: <https://github.com/brunobraga/termsaver/issues>

* Fork this project: <https://github.com/brunobraga/termsaver/fork>
    
Uninstall
----------

### Using Apt (Advanced Packaging Tool) or PPA (Personal Package Archive)

        sudo apt-get remove termsaver


### Using Pip (Pip Install Packages, for Python Package Index)

        sudo pip uninstall termsaver


### Manual Uninstall

Just remove manually the following files:

        # For Linux boxes
        rm -rvf /usr/local/bin/termsaver
        
        # change your python version/location here
        rm -rvf /usr/local/lib/python3.x/dist-packages/termsaver* 
        
        rm -rvf /usr/local/share/man/man1/termsaver.1 
        find /usr/local/share/locale/ -name "termsaver.mo" -exec rm -rfv {} \; 

If the actuall location differ from the above, it might be worth it to just
run the find command and look for them yourself (should not be hard):

        find /usr/ -name "*termsaver*" 
