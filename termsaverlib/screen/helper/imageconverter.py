from PIL import Image
import os
import io

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
            r = requests
            image = Image.open(io.BytesIO(r.content))
        else:
            image = Image.open(self.source_path)
        
        return image
    
    def process_image(self, twidth, theight):
        
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

        return image.resize((width, height), Image.LANCZOS)
    
    def convert_image(self, source_path, height, width, options = []):
        self.source_path = source_path
        self.options = options
        image = self.process_image(height, width)
        #specter = ' .:;+=xX$&'
        specter = ' ░▒▓█'
        wide = 2 # self.options['wide']
        chars = False # self.options['chars']

        if chars != False:
            specter = chars
        
        # if self.options['contrast'] == True:
        #     specter = ' ░▒▓█'

        # if self.options['reverse'] == True:
        #     specter = specter[::-1]
        
        # per img/frame
        image = image.convert('RGBA')
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
            
        # if self.options['rotate'] != False:
        #     orientation = 1 if self.options['rotate'] == left else -1
        #     rotated = zip(*string.split('\n')[::orientation])
        #     string = []
        #     for row in rotated:
        #         string.append(''.join(list(row)))
            
        #     string = '\n'.join(string)
        
        return string