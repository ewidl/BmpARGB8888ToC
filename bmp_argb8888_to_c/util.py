from bmp_argb8888_to_c.template import TEMPLATE_LINE_SEPARATOR, ELEMENT_SEPARATOR

from re import match

def convert_little_endian_hex_to_decimal(str_hex):
    len_hex = len(str_hex)

    # Require even number of hexadecimal digits, because 2 hexadecimal digits are need for each byte.
    if len_hex%2:
        raise RuntimeError('Hex string must have an even number of digits')

    # Extract each byte (=2 hexadecimal digits), multiply with its base, and add up.
    val_dec = 0
    for i in range(0, len_hex, 2):
        val_dec += int(str_hex[i:i+2], 16) * pow(16,i)

    return val_dec

def convert_decimal_to_little_endian_hex(val_dec, n_bytes=4):
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

def convert_hex_string_to_c_array_elements(str_hex):
    len_hex = len(str_hex)

    # Require even number if hexadecimal digits, because 2 hexadecimal digits are need for each byte.
    if len_hex%2:
        raise RuntimeError('Hex string must have an even number of digits')

    # Add each byte (=2 hexadecimal digits) as inidvidual hex string (e.g., 0xFF).
    array = []
    for i in range(0, len_hex, 2):
        array.append( 
            '0x{data}'.format(data=str_hex[i:i+2])
            )

    return array

def c_compatible_name(str_name):
    return ''.join([c for c in str_name if match(r'\w', c)])
    
def blockify(str_list, n=12):
    # Individual C array element.
    sub = str_list.split(ELEMENT_SEPARATOR)
    
    # Blocked lines of C array elements.
    lines = [ELEMENT_SEPARATOR.join(sub[i:i+n]) for i in range(0, len(sub)-1, n)]        

    # Return blocked C array.
    return TEMPLATE_LINE_SEPARATOR.join(lines)
