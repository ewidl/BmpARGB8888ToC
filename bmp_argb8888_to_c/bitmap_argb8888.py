from bmp_argb8888_to_c.util import convert_little_endian_hex_to_decimal

from binascii import hexlify
from pathlib import Path

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
        header_size = convert_little_endian_hex_to_decimal(self.header_size)
        if not 56 == header_size:
            raise RuntimeError('Unexpected DIB header: ' +
                f'expected type BITMAPV3INFOHEADER (size=56), got size={header_size}')

        bits_per_pixel = convert_little_endian_hex_to_decimal(self.bits_per_pixel)
        if not 32 == bits_per_pixel:
            raise RuntimeError('Wrong number of bits per pixel: ' +
                f'expected type 32, got {bits_per_pixel}')

        # Get (decimal) value for pixel array offset. Expected pixel array offset for ARGB8888 is 70 (no gap).
        offset_pixel_array = convert_little_endian_hex_to_decimal(self.offset_pixel_array)

        # Set gap (in case pixel array offset is more than 70).
        self.gap = '00' * (offset_pixel_array - 70)

        # Retrieve pixel array.
        self.pixel_array = hexData[2*offset_pixel_array:]
