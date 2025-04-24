"""
Copyright © 2024-2025  Bartłomiej Duda
License: GPL-3.0 License
"""

from reversebox.image.common import get_stride_value

# fmt: off

# PSP Texture Swizzling
# Note: Input data has to be 16-bytes aligned to be processed correctly!


def _convert_psp(image_data: bytes, img_width: int, img_height: int, bpp: int, swizzle_flag: bool) -> bytes:
    converted_data = bytearray(len(image_data))
    output_offset: int = 0
    stride: int = get_stride_value(img_width, bpp)
    row_blocks: int = stride // 16

    for y in range(img_height):
        for x in range(stride):
            block_x = x // 16
            block_y = y // 8
            block_index = block_x + (block_y * row_blocks)
            block_address = block_index * 16 * 8
            if not swizzle_flag:
                converted_data[output_offset] = image_data[block_address + (x - block_x * 16) + ((y - block_y * 8) * 16)]
            else:
                converted_data[block_address + (x - block_x * 16) + ((y - block_y * 8) * 16)] = image_data[output_offset]
            output_offset += 1

    return converted_data


def unswizzle_psp(image_data: bytes, img_width: int, img_height: int, bpp: int) -> bytes:
    return _convert_psp(image_data, img_width, img_height, bpp, False)


def swizzle_psp(image_data: bytes, img_width: int, img_height: int, bpp: int):
    return _convert_psp(image_data, img_width, img_height, bpp, True)
