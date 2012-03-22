<!-- 
###############################################################################
#
# file:     README
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

**<http://termsaver.info>**

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

  * Linux, or Mac
  * Python 2.4+ (and < 3.x)

**Note**: Windows support is in the roadmap.


Installation
------------

For those without the time or patience to scan through the rest of this 
document, here is the installation procedure, plain and simple:

1. Download the Source 
[here](https://github.com/brunobraga/termsaver/downloads)
2. Unpack it
     
        tar -zxvf termsaver-{version}.tar.gz

3. Install it

        sudo python setup.py install 

4. All done! 


Features
--------

The TermSaver is a very simple application, built with the idea to allow more 
screensavers to be added to its core. Developers, please read the section below. 

The current published screensavers are:

#### Ascii Art Farts

This is a screensaver that displays ascii art from asciiartfarts.com 
RSS feed in an animation format. 

#### Dot

A extremely simple screensaver, created more with the idea to guide developers 
on how to use the termsaver libraries to build their own, and help grow the 
termsaver screensaver gallery in future.

This screensaver only displays a running dot that appears in random locations 
and sizes.

#### Jokes For All

This is a screensaver that displays recent jokes from <http://jokes4all.net>
website, from its hourly updated [RSS](http://en.wikipedia.org/wiki/RSS) feed.

#### Programmer

This is a screensaver that displays source code from a specified path in
visual animation.

#### Quotes For All

This is a screensaver that displays recent quotes from <http://quotes4all.net>
website, from its hourly updated [RSS](http://en.wikipedia.org/wiki/RSS) feed.

#### Random Text

This is a screensaver that displays a text (your name, or whatever) on a 
 randomized position of the screen, changing position every N seconds.

#### Request for Change

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

This is a screensaver that displays a digital clock using ascii letters..

 - - -

**Disclaimer Note**: termsaver holds no responsibility for the contents offered 
by third-parties, nor it has controls to filter them. Use it at your own risk.


Developers
----------

A more detailed guideline for developers willing to jump in and create 
screensavers for termsaver will be available soon.


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

Let us know you want to help: <support@termsaver.info>


### Screensavers (plugin)

As of this moment, all screensavers are part of the termsaver library, but it
was initially designed to predict the implementation of additional screensavers
as plug-ins to the main application. 

This is, however, not fully defined, so feel free to start now by forking this
code and implementing it directly inside termsaver. Your contribution will be
reflected in the list of authors of this application.


### Submit a bug

If you find any errors in this application, you are more than welcome to 
participate. You can:

* report the bug: <https://github.com/brunobraga/termsaver/issues>

* Fork this project: <https://github.com/brunobraga/termsaver/fork>
    
Uninstall
----------

To uninstall termsaver, you will need to run the installation command with 
some additional arguments:

    # Step 1 - re-install creating a manifest file
    sudo python setup.py install --record /tmp/termsaver.install.record.txt

    # Step 2 - uninstall referencing the manifest file
    sudo python setup.py uninstall --manifest /tmp/termsaver.install.record.txt
    
    # Done!

