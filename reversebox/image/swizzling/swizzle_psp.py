"""
Copyright © 2024-2025  Bartłomiej Duda
License: GPL-3.0 License
"""

from reversebox.image.common import get_stride_value, get_stride_value_psp

# fmt: off

# PSP Texture Swizzling


def unswizzle_psp(image_data: bytes, img_width: int, img_height: int, bpp: int) -> bytes:
    bytes_per_pixel: int = bpp // 8
    stride: int = get_stride_value_psp(img_width, bpp)
    unswizzled_data = bytearray(len(image_data))
    padded_data_offset: int = 0
    unswizzled_data_offset: int = 0
    row_blocks: int = stride // 16

    # unswizzle logic
    for y in range(img_height):
        for x in range(stride):
            block_x = x // 16
            block_y = y // 8
            block_index = block_x + (block_y * row_blocks)
            block_address = block_index * 16 * 8
            local_position: int = (x % 16) + (y % 8) * 16
            unswizzled_data[unswizzled_data_offset] = image_data[block_address + local_position]
            unswizzled_data_offset += 1

    # padding logic
    unswizzled_padded_data = bytearray(img_width * img_height * bytes_per_pixel)
    for y in range(img_height):
        row_start = y * stride
        row_end = row_start + img_width * bytes_per_pixel
        unswizzled_padded_data[padded_data_offset: padded_data_offset + img_width * bytes_per_pixel] = unswizzled_data[row_start: row_end]
        padded_data_offset += img_width * bytes_per_pixel

    return unswizzled_padded_data


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
