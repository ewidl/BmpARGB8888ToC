from bmp_argb8888_to_c.template import TEMPLATE, TEMPLATE_LINE_SEPARATOR, ELEMENT_SEPARATOR

from binascii import hexlify
from pathlib import Path
from re import match

class BitmapARGB8888:
    '''
    Read content of bitmap file in ARGB8888 format and convert to C array.
    '''

    def __init__(self, file_name):
        # File path.
        self.file_name = Path(file_name).resolve(strict = True)

        # Retrieve content of binary file as string of hexadecimal digits.
        file = open(self.file_name, 'rb')
        hexData = hexlify(file.read()).decode('utf-8').upper()

        # Retrieve bitmap file header.
        self.signature = hexData[0:4]
        self.file_size = hexData[4:12]
        self.reserved = hexData[12:20]
        self.offset_pixel_array = hexData[20:28]

        # Sanity check for signature.
        if not self.signature == '424D':
            raise RuntimeError(f'Invalid signature: {self.signature}')

        # Retrieve DIB header.
        self.header_size = hexData[28:36]
        self.image_width = hexData[36:44]
        self.image_height = hexData[44:52]
        self.num_color_planes = hexData[52:56]
        self.bits_per_pixel = hexData[56:60]
        self.compression = hexData[60:68]
        self.image_size = hexData[68:76]
        self.x_pixels_per_meter = hexData[76:84]
        self.y_pixels_per_meter = hexData[84:92]
        self.color_table = hexData[92:100]
        self.important_color = hexData[100:108]
        self.resolution_units = hexData[108:112]
        self.padding = hexData[112:116]
        self.fill_direction = hexData[116:120]
        self.halftoning_algo = hexData[120:124]
        self.halftoning_param_1 = hexData[124:132]
        self.halftoning_param_2 = hexData[132:140]

        # Sanity check for DIB header.
        header_size = BitmapARGB8888._convert_little_endian_hex_to_decimal(self.header_size)
        if not 56 == header_size:
            raise RuntimeError('Unexpected DIB header: ' +
                f'expected type BITMAPV3INFOHEADER (size=56), got size={header_size}')

        bits_per_pixel = BitmapARGB8888._convert_little_endian_hex_to_decimal(self.bits_per_pixel)
        if not 32 == bits_per_pixel:
            raise RuntimeError('Wrong number of bits per pixel: ' +
                f'expected type 32, got {bits_per_pixel}')

        # Get (decimal) value for pixel array offset. Expected pixel array offset for ARGB8888 is 70 (no gap).
        offset_pixel_array = BitmapARGB8888._convert_little_endian_hex_to_decimal(self.offset_pixel_array)

        # Set gap (in case pixel array offset is more than 70).
        self.gap = '00' * (offset_pixel_array - 70)

        # Retrieve pixel array.
        self.pixel_array = hexData[2*offset_pixel_array:]

    def as_c_array(self):
        '''
        Convert bitmap data to C array.
        '''
        # Generate C-compliant name from file name.
        name = BitmapARGB8888._c_compatible_name(self.file_name.stem)

        # Define guard expression.
        guard = 'INCLUDE_{name}_H_'.format(name = name.upper())

        # Get (decimal) value of file size.
        array_size = BitmapARGB8888._convert_little_endian_hex_to_decimal(self.file_size)

        # Use short version for long function name.
        convert = BitmapARGB8888._convert_hex_string_to_c_array_elements

        return TEMPLATE.format(
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
            pixel_array = BitmapARGB8888._blockify(convert(self.pixel_array)),
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
        name = BitmapARGB8888._c_compatible_name(self.file_name.stem)

        # Define guard expression.
        guard = 'INCLUDE_{name}_H_'.format(name = name.upper())

        # Get (decimal) value of file size.
        array_size = BitmapARGB8888._convert_little_endian_hex_to_decimal(self.file_size)

        # Add a gap so that the pixel array is 4-byte memory aligned.
        offset = BitmapARGB8888._convert_little_endian_hex_to_decimal(self.offset_pixel_array)
        delta = offset%4
        new_gap = self.gap + '00' * delta
        new_offset_pixel_array = BitmapARGB8888._convert_decimal_to_little_endian_hex(offset + delta)
        new_array_size = array_size + delta
        new_file_size = BitmapARGB8888._convert_decimal_to_little_endian_hex(new_array_size)

        # Use short version for long function name.
        convert = BitmapARGB8888._convert_hex_string_to_c_array_elements

        return TEMPLATE.format(
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
            pixel_array = BitmapARGB8888._blockify(convert(self.pixel_array)),
        )

    def _convert_little_endian_hex_to_decimal(str_hex):
        len_hex = len(str_hex)

        # Require even number of hexadecimal digits, because 2 hexadecimal digits are need for each byte.
        if len_hex%2:
            raise RuntimeError('Hex string must have an even number of digits')

        # Extract each byte (=2 hexadecimal digits), multiply with its base, and add up.
        val_dec = 0
        for i in range(0, len_hex, 2):
            val_dec += int(str_hex[i:i+2], 16) * pow(16,i)

        return val_dec

    def _convert_decimal_to_little_endian_hex(val_dec, n_bytes=4):
        # Get hexadecimal value as big-endian.
        str_hex = hex(val_dec)[2:].upper()

        # Check if hex value fits into the given number of bytes.
        if len(str_hex) > 2*n_bytes:
            raise RuntimeError(f'Decimal value does not fit into {n_bytes} byte(s)')

        # Add padding characters (empty bytes) to the left.
        str_hex_padding = str_hex.rjust(2*n_bytes, '0')

        # Iterate bytes and store bytes in reverse. 
        list_str_hex_padding_little_endian = \
            [str_hex_padding[i:i+2] for i in reversed(range(0, 2*n_bytes, 2))]

        # Concatenate bytes in reverse order.
        return ''.join(list_str_hex_padding_little_endian)

    def _convert_hex_string_to_c_array_elements(str_hex):
        len_hex = len(str_hex)

        # Require even number if hexadecimal digits, because 2 hexadecimal digits are need for each byte.
        if len_hex%2:
            raise RuntimeError('Hex string must have an even number of digits')

        # Concatenate each byte (=2 hexadecimal digits) as inidvidual hex strings (e.g., 0xFF).
        str_arr = ''
        for i in range(0, len_hex, 2):
            str_arr += '0x{data},{sep}'.format(
                data=str_hex[i:i+2], sep=ELEMENT_SEPARATOR
            )

        return str_arr

    def _c_compatible_name(str_name):
        return ''.join([c for c in str_name if match(r'\w', c)])
        
    def _blockify(str_list, n=12):
        # Individual C array element.
        sub = str_list.split(ELEMENT_SEPARATOR)
        
        # Blocked lines of C array elements.
        lines = [ELEMENT_SEPARATOR.join(sub[i:i+n]) for i in range(0, len(sub)-1, n)]        

        # Return blocked C array.
        return TEMPLATE_LINE_SEPARATOR.join(lines)
