from bmp_argb8888_to_c.bitmap_to_array import BitmapToArray
from bmp_argb8888_to_c.bitmap_to_font import BitmapToFont

import argparse
import sys

def argb8888_to_c():
    '''
    Console script for converting bitmap data to C array.
    '''
    # Command line parser.
    parser = argparse.ArgumentParser(
        description = 'Convert bitmap data to C array.'
    )

    required = parser.add_argument_group( 'required named arguments' )

    required.add_argument(
        'input_file',
        action = 'store',
        metavar = 'INPUT_FILE',
        help = 'input bitmap file (ARGB8888-formatted)'
    )

    parser.add_argument(
        '-o', '--output-file',
        default = [],
        action = 'store',
        metavar = 'OUTPUT_FILE',
        help = 'output file name'
    )

    args = parser.parse_args()

    try:

        bmp = BitmapToArray(args.input_file)
        bmp_file = bmp.file_name

        out = bmp.as_c_array()
        out_file = args.output_file or (bmp_file.stem + '.h')

        with open(out_file, 'w') as file:
            file.write(out)

        print(f'Output written to {out_file}')
        sys.exit( 0 )

    except Exception as err:

        print( str( err ) )
        sys.exit( 1 )

def argb8888_to_c_aligned():
    '''
    Console script for converting bitmap data to C array with 4-byte aligned pixel array.
    '''
    # Command line parser.
    parser = argparse.ArgumentParser(
        description = 'Convert bitmap data to C array with 4-byte aligned pixel array.'
    )

    required = parser.add_argument_group( 'required named arguments' )

    required.add_argument(
        'input_file',
        action = 'store',
        metavar = 'INPUT_FILE',
        help = 'input bitmap file (ARGB8888-formatted)'
    )

    parser.add_argument(
        '-o', '--output-file',
        default = [],
        action = 'store',
        metavar = 'OUTPUT_FILE',
        help = 'output file name'
    )

    args = parser.parse_args()

    try:

        bmp = BitmapToArray(args.input_file)
        bmp_file = bmp.file_name

        out = bmp.as_c_array_aligned()
        out_file = args.output_file or (bmp_file.stem + '.h')

        with open(out_file, 'w') as file:
            file.write(out)

        print(f'Output written to {out_file}')
        sys.exit( 0 )

    except Exception as err:

        print( str( err ) )
        sys.exit( 1 )

def argb8888_to_c_font():
    '''
    Console script for converting bitmap data to C array for anti-aliased fonts.
    '''
    # Command line parser.
    parser = argparse.ArgumentParser(
        description = 'Convert bitmap data to C array for anti-aliased fonts.'
    )

    required = parser.add_argument_group( 'required named arguments' )

    required.add_argument(
        'input_file',
        action = 'store',
        metavar = 'INPUT_FILE',
        help = 'input bitmap file (ARGB8888-formatted)'
    )

    required.add_argument(
        'font_height',
        type = int, 
        action = 'store',
        metavar = 'FONT_HEIGHT',
        help = 'font height'
    )

    required.add_argument(
        'font_width',
        type = int, 
        action = 'store',
        metavar = 'FONT_WIDTH',
        help = 'font width'
    )

    parser.add_argument(
        '-o', '--output-file',
        default = [],
        action = 'store',
        metavar = 'OUTPUT_FILE',
        help = 'output file name'
    )

    args = parser.parse_args()

    try:

        bmp = BitmapToFont(args.input_file, args.font_height, args.font_width)
        bmp_file = bmp.file_name

        out = bmp.as_c_font()
        out_file = args.output_file or (bmp_file.stem + '.c')

        with open(out_file, 'w') as file:
            file.write(out)

        print(f'Output written to {out_file}')
        sys.exit( 0 )

    except Exception as err:

        print( str( err ) )
        sys.exit( 1 )
