"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

from reversebox.image.common import get_stride_value

# fmt: off


def unswizzle_psp(image_data: bytes, img_width: int, img_height: int, bpp: int) -> bytes:
    unswizzled_data = bytearray(len(image_data))
    output_offset: int = 0
    stride: int = get_stride_value(img_width, bpp)
    row_blocks = stride // 16

    for y in range(img_height):
        for x in range(stride):
            block_x = x // 16
            block_y = y // 8
            block_index = block_x + (block_y * row_blocks)
            block_address = block_index * 16 * 8
            unswizzled_data[output_offset] = image_data[block_address + (x - block_x * 16) + ((y - block_y * 8) * 16)]
            output_offset += 1

    return unswizzled_data


def swizzle_psp(image_data: bytes, img_width: int, img_height: int, bpp: int):
    swizzled_data = bytearray(len(image_data))
    source_offset: int = 0
    stride: int = get_stride_value(img_width, bpp)
    row_blocks = stride // 16

    for y in range(img_height):
        for x in range(stride):
            block_x = x // 16
            block_y = y // 8
            block_index = block_x + (block_y * row_blocks)
            block_address = block_index * 16 * 8
            swizzled_data[block_address + (x - block_x * 16) + ((y - block_y * 8) * 16)] = image_data[source_offset]
            source_offset += 1

    return swizzled_data
