# Convert ARGB8888 bitmaps to C arrays

## Installation

Install with `pip` from the terminal:

```
pip install .
```

## Usage

The package provides console scripts for converting bitmaps:

- Convert bitmap data to C array:
  ```
  argb8888_to_c [-h] -i INPUT_FILE [-o EXTRA_FILE]
  ```

- Convert bitmap data to C array with 4-byte aligned pixel array:
  ```
  argb8888_to_c_aligned [-h] -i INPUT_FILE [-o OUTPUT FILE]
  ```

## Implementation details

When converting a bitmap to C an array, some applications require the [pixel array](https://en.wikipedia.org/wiki/BMP_file_format#Pixel_storage) to have a specific [memory alignment](https://www.songho.ca/misc/alignment/dataalign.html).
For example, the [STM32CubeF7 MCU Firmware Package](https://github.com/STMicroelectronics/STM32CubeF7) requires ARGB8888-formatted pixel arrays to be 4-byte aligned.

However, for ARGB8888 the default offset of the pixel array is 70. 
Therefore, even if the start of the overall bitmap data is 4-byte aligned in memory, the start of the pixel array is not.
When converting the bitmap file to a C array using standard tools (e.g., [Bin2C](https://www.segger.com/free-utilities/bin2c/)), the resulting pixel array is therefore not properly aligned.

Packag `bmp_argb8888_to_c` solves this problem by adding an additional gap of 2 bytes between the [DIB header](https://en.wikipedia.org/wiki/BMP_file_format#DIB_header_(bitmap_information_header)) and the pixel array when converting the bitmap.
