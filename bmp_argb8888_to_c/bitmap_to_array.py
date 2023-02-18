from bmp_argb8888_to_c.bitmap_argb8888 import BitmapARGB8888
from bmp_argb8888_to_c.template import ARRAY_TEMPLATE
from bmp_argb8888_to_c.util import *

class BitmapToArray(BitmapARGB8888):
    '''
    Read content of bitmap file in ARGB8888 format and convert to C array.
    '''

    def as_c_array(self):
        '''
        Convert bitmap data to C array.
        '''
        # Generate C-compliant name from file name.
        name = c_compatible_name(self.file_name.stem)

        # Define guard expression.
        guard = 'INCLUDE_{name}_H_'.format(name = name.upper())

        # Get (decimal) value of file size.
        array_size = convert_little_endian_hex_to_decimal(self.file_size)

        # Define function for concatenation.
        separator = ',{}'.format(ELEMENT_SEPARATOR)
        convert = lambda x: separator.join(convert_hex_string_to_c_array_elements(x))

        return ARRAY_TEMPLATE.format(
            name = name,
            guard = guard,
            array_size = array_size,
            signature = convert(self.signature),
            file_size = convert(self.file_size),
            reserved = convert(self.reserved),
            offset_pixel_array = convert(self.offset_pixel_array),
            header_size = convert(self.header_size),
            image_width = convert(self.image_width),
            image_height = convert(self.image_height),
            num_color_planes = convert(self.num_color_planes),
            bits_per_pixel = convert(self.bits_per_pixel),
            compression = convert(self.compression),
            image_size = convert(self.image_size),
            x_pixels_per_meter = convert(self.x_pixels_per_meter),
            y_pixels_per_meter = convert(self.y_pixels_per_meter),
            color_table = convert(self.color_table),
            important_color = convert(self.important_color),
            resolution_units = convert(self.resolution_units),
            padding = convert(self.padding),
            fill_direction = convert(self.fill_direction),
            halftoning_algo = convert(self.halftoning_algo),
            halftoning_param_1 = convert(self.halftoning_param_1),
            halftoning_param_2 = convert(self.halftoning_param_2),
            gap = convert(self.gap),
            pixel_array = blockify(convert(self.pixel_array)),
        )

    def as_c_array_aligned(self):
        '''
        Convert bitmap data to C array with 4-byte memory aligned pixel array.
        
        For ARGB8888, the default offset of the pixel array is 70. Therefore, even if
        the start of the overall bitmap data is 4-byte aligned in memory, the start of
        the pixel array is not. One solution to this problem is to add a gap of 2 bytes
        between the DIB header and the pixel array when converting the bitmap.
        '''
        # Generate C-compliant name from file name.
        name = c_compatible_name(self.file_name.stem)

        # Define guard expression.
        guard = 'INCLUDE_{name}_H_'.format(name = name.upper())

        # Get (decimal) value of file size.
        array_size = convert_little_endian_hex_to_decimal(self.file_size)

        # Add a gap so that the pixel array is 4-byte memory aligned.
        offset = convert_little_endian_hex_to_decimal(self.offset_pixel_array)
        delta = offset % 4
        new_gap = self.gap + '00' * delta
        new_offset_pixel_array = convert_decimal_to_little_endian_hex(offset + delta)
        new_array_size = array_size + delta
        new_file_size = convert_decimal_to_little_endian_hex(new_array_size)

        # Define function for concatenation.
        separator = ',{}'.format(ELEMENT_SEPARATOR)
        convert = lambda x: separator.join(convert_hex_string_to_c_array_elements(x))

        return ARRAY_TEMPLATE.format(
            name = name,
            guard = guard,
            array_size = new_array_size,
            signature = convert(self.signature),
            file_size = convert(new_file_size),
            reserved = convert(self.reserved),
            offset_pixel_array = convert(new_offset_pixel_array),
            header_size = convert(self.header_size),
            image_width = convert(self.image_width),
            image_height = convert(self.image_height),
            num_color_planes = convert(self.num_color_planes),
            bits_per_pixel = convert(self.bits_per_pixel),
            compression = convert(self.compression),
            image_size = convert(self.image_size),
            x_pixels_per_meter = convert(self.x_pixels_per_meter),
            y_pixels_per_meter = convert(self.y_pixels_per_meter),
            color_table = convert(self.color_table),
            important_color = convert(self.important_color),
            resolution_units = convert(self.resolution_units),
            padding = convert(self.padding),
            fill_direction = convert(self.fill_direction),
            halftoning_algo = convert(self.halftoning_algo),
            halftoning_param_1 = convert(self.halftoning_param_1),
            halftoning_param_2 = convert(self.halftoning_param_2),
            gap = convert(new_gap),
            pixel_array = blockify(convert(self.pixel_array)),
        )

