# Separator for C array elements.
ELEMENT_SEPARATOR = str(' ')

# Separator for lines in template.
TEMPLATE_LINE_SEPARATOR = str('\n  ')

# Template for C array (with include guards).
TEMPLATE = '''
#ifndef {guard}
#define {guard}

const unsigned char {name}[{array_size}UL + 1] __attribute__ ((aligned (4)))
{{
  // BITMAP FILE HEADER
  {signature}// SIGNATURE
  {file_size}// FILE SIZE
  {reserved}// RESERVED
  {offset_pixel_array}// PIXEL ARRAY OFFSET

  // DIB HEADER (BITMAPV3INFOHEADER)
  {header_size}// HEADER SIZE
  {image_width}// IMAGE WIDTH
  {image_height}// IMAGE HEIGHT
  {num_color_planes}// NUMBER OF COLOR PLANES
  {bits_per_pixel}// NUMBER OF BITS PER PIXEL
  {compression}// COMPRESSION METHOD
  {image_size}// SIZE OF THE RAW BITMAP DATA
  {x_pixels_per_meter}// HORIZONTAL RESOLUTION OF THE IMAGE
  {y_pixels_per_meter}// VERTICAL RESOLUTION OF THE IMAGE
  {color_table}// NUMBER OF COLORS IN THE COLOR PALETTE
  {important_color}// NUMBER OF IMPORTANT COLORS USED
  {resolution_units}// UNITS FOR THE HORIZONTAL AND VERTICAL RESOLUTIONS
  {padding}// PADDING
  {fill_direction}// DIRECTION IN WHICH THE BITS FILL THE BITMAP
  {halftoning_algo}// HALFTONING ALGORITHM
  {halftoning_param_1}// HALFTONING PARAMETER 1
  {halftoning_param_2}// HALFTONING PARAMETER 2

  {gap}// GAP

  // PIXEL ARRAY
  {pixel_array}

  0x00 // EOF
}};

#endif // {guard}
'''
