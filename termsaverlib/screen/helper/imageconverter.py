###############################################################################
#
# file:     imageconverter.py
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

from PIL import Image
import os
import io
import requests

class ImageConverter:
    source_path = False
    options = False
    
    def is_link(self):
        if 'http' == self.source_path[0:4].lower():
            return True
        return False
    
    def image_type(self):
        extension = self.source_path[-4:].lower()
        imgtype = extension.strip('.')

        return imgtype
    
    def get_image(self):
        if self.is_link():
            r = requests.get(self.source_path, stream=True)
            image = Image.open(io.BytesIO(r.content))
        else:
            image = Image.open(self.source_path)
        
        return image
    
    def process_image(self, twidth, theight, scale = 1):
        
        image = self.get_image()
        image_type = self.image_type()

        width = image.size[0]
        height = image.size[1]

        twidth -= 1
        theight -= 1

        ri = width / height
        rs = twidth / theight

        if rs > ri:
            width = width * theight / height
            height = theight
        else:
            width  = twidth
            height = height * twidth / width
        
        width = int(width)
        height = int(height)

        return image.resize((width * scale, height * scale), Image.LANCZOS)
    
    def convert_image(self, source_path, height, width, options):
        self.source_path = source_path
        self.options = options

        if 'scale' in self.options:
            scale = self.options['scale']
        else:
            scale = 1

        image = self.process_image(height, width, scale)
        specter = ' .:;+=xX$&'

        if 'wide' in self.options:
            wide = self.options['wide']
        else: 
            wide = 2
       
        if 'contrast' in self.options:
            specter = ' ░▒▓█'

        if 'customcharset' in self.options:
            specter = self.options['customcharset']

        if 'invert' in self.options:
            specter = specter[::-1]
        
        # per img/frame
        image = image.convert('RGB')
        string = ''
        width,height = image.size
        last_row = 0
        contrast_levels = []
        contrast_gap = 255 / len(specter)
        for gap in range(len(specter)):
            contrast_levels.append(contrast_gap * gap)
        
        for y in range(height):
            for x in range(width):
                if y != last_row:
                    string += '\n'
                    last_row += 1
                try:
                    r, g, b = image.getpixel((x,y))
                except:
                    r, g, b, a = image.getpixel((x,y))
                pixel_value = (r * 0.3 + g * 0.59 + b * 0.11)
                levels = []
                for level in contrast_levels:
                    levels.append(abs(pixel_value - level))
                character = specter[levels.index(min(levels))] * wide
                string += character
        
        return string