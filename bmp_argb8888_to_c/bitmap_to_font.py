from bmp_argb8888_to_c.bitmap_argb8888 import BitmapARGB8888
from bmp_argb8888_to_c.template import FONT_ARRAY_TEMPLATE, SINGLE_FONT_TEMPLATE
from bmp_argb8888_to_c.util import *

class BitmapToFont(BitmapARGB8888):
    '''
    Read content of a bitmap file in ARGB8888 format and convert it to a C array for 
    anti-aliased monospace fonts.
    
    The extracted array contains the transparency information for each pixel of each
    font (from top left to bottom right for each pixel). This can be used as mask for 
    creating anit-aliased fonts on a screen.
    
    The expected input is a bitmap with all the fonts in a single row (in ASCII-order).
    '''

    def __init__(self, file_name, font_height, font_width):
        super().__init__(file_name)

        # Sanity check.
        line_width = convert_little_endian_hex_to_decimal(self.image_width)
        if not 0 == line_width % font_width:
            raise RuntimeError(f'Image width ({line_width}) must be a multiple of font with ({font_width}).')

        image_height = convert_little_endian_hex_to_decimal(self.image_height)
        if not image_height == font_height:
            raise RuntimeError(f'Image height ({image_height}) must be same as font height ({font_height}).')

        self.line_width = line_width
        self.font_height = font_height
        self.font_width = font_width
        self.n_fonts = int(line_width / font_width)

    def as_c_font(self):
        '''
        Convert bitmap data to C array for anti-aliased fonts.
        '''
        # Extract all bytes with transparency information (every 4th
        # byte) in the order they appear in the pixel array, i.e.,
        # from bottom left to top right (image containing all fonts).
        transparency = convert_hex_string_to_c_array_elements(self.pixel_array)[3::4]

        # Create empty list for each font.
        fonts = [[] for _ in range(self.n_fonts)]

        # Extract transparency information in correct order for each
        # individual font. Resulting order will be from top left to 
        # bottom right (for each font).
        for line in reversed(range(self.font_height)):
            for i in range(self.n_fonts):
                start = line * self.line_width + i * self.font_width
                stop = start + self.font_width
                fonts[i].extend(transparency[start:stop])

        # Define function for concatenation.
        separator = ',{}'.format(ELEMENT_SEPARATOR)
        convert = lambda x: blockify(separator.join(x), n=self.font_width) + separator

        # Generate C sub-array for each font.
        single_font_arrays = [
            SINGLE_FONT_TEMPLATE.format(
                font_data = convert(f), pos = i * self.font_width * self.font_height
                ) for (i, f) in enumerate(fonts)
            ]
        
        # Generate C-compliant name from file name.
        name = c_compatible_name(self.file_name.stem)

        # Define guard expression.
        guard = 'INCLUDE_{name}_H_'.format(name = name.upper())

        # Generate C array for complete collection of fonts.
        return FONT_ARRAY_TEMPLATE.format(
            name = name,
            font_width = self.font_width,
            font_heigth = self.font_height,
            fonts_array = ''.join(single_font_arrays),
            guard = guard,
        )
