from bmp_argb8888_to_c.bitmap_argb8888 import BitmapARGB8888

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
        '-i', '--input-file',
        action = 'store',
        required = True,
        metavar = 'INPUT_FILE',
        help = 'input bitmap file (ARGB8888-formatted)'
    )

    parser.add_argument(
        '-o', '--output-file',
        default = [],
        action = 'store',
        metavar = 'OUTPUT FILE',
        help = 'additional file to be added to the orchestrator Docker image'
    )

    args = parser.parse_args()

    try:

        bmp = BitmapARGB8888(args.input_file)
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
    Console script for converting bitmap data to C array with 4-byte aligned pixel array..
    '''
    # Command line parser.
    parser = argparse.ArgumentParser(
        description = 'Convert bitmap data to C array with 4-byte aligned pixel array.'
    )

    required = parser.add_argument_group( 'required named arguments' )

    required.add_argument(
        '-i', '--input-file',
        action = 'store',
        required = True,
        metavar = 'INPUT_FILE',
        help = 'input bitmap file (ARGB8888-formatted)'
    )

    parser.add_argument(
        '-o', '--output-file',
        default = [],
        action = 'store',
        metavar = 'OUTPUT FILE',
        help = 'additional file to be added to the orchestrator Docker image'
    )

    args = parser.parse_args()

    try:

        bmp = BitmapARGB8888(args.input_file)
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
