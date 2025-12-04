"""
Copyright © 2024-2025  Bartłomiej Duda
License: GPL-3.0 License
"""

from reversebox.image.common import get_stride_value, get_stride_value_psp

# fmt: off

# PSP Texture Swizzling

# Note: Data must be padded to 16 bytes to unswizzle correctly.
# Use "psp_image_padding" function to adjust image data.


def unswizzle_psp(image_data: bytes, img_width: int, img_height: int, bpp: int) -> bytes:
    stride: int = get_stride_value_psp(img_width, bpp)
    unswizzled_data = bytearray(len(image_data))
    unswizzled_data_offset: int = 0
    row_blocks: int = stride // 16

    for y in range(img_height):
        for x in range(stride):
            block_x = x // 16
            block_y = y // 8
            block_index = block_x + (block_y * row_blocks)
            block_address = block_index * 16 * 8
            local_position: int = (x % 16) + (y % 8) * 16
            unswizzled_data[unswizzled_data_offset] = image_data[block_address + local_position]
            unswizzled_data_offset += 1

    return unswizzled_data


def swizzle_psp(image_data: bytes, img_width: int, img_height: int, bpp: int):
    stride: int = get_stride_value(img_width, bpp)
    padded_stride: int = get_stride_value_psp(img_width, bpp)
    padded_height: int = (img_height + 7) & ~7
    swizzled_data: bytearray = bytearray(padded_stride * padded_height)
    row_blocks: int = padded_stride // 16

    for y in range(img_height):
        for x in range(stride):
            block_x = x // 16
            block_y = y // 8
            block_index = block_x + block_y * row_blocks
            block_address = block_index * 16 * 8
            local_x = x % 16
            local_y = y % 8
            swizzled_data[block_address + local_y * 16 + local_x] = image_data[y * stride + x]

    return bytes(swizzled_data)
