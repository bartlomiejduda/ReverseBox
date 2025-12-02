"""
Copyright © 2024-2025  Bartłomiej Duda
License: GPL-3.0 License
"""

from reversebox.image.common import get_stride_value_psp

# fmt: off

# PSP Texture Swizzling


def _convert_psp(image_data: bytes, img_width: int, img_height: int, bpp: int, swizzle_flag: bool) -> bytearray:
    converted_data = bytearray(len(image_data))
    output_offset: int = 0
    stride: int = get_stride_value_psp(img_width, bpp)
    row_blocks: int = stride // 16

    for y in range(img_height):
        for x in range(stride):
            block_x = x // 16
            block_y = y // 8
            block_index = block_x + (block_y * row_blocks)
            block_address = block_index * 16 * 8
            local_position: int = (x % 16) + (y % 8) * 16

            if not swizzle_flag:
                converted_data[output_offset] = image_data[block_address + local_position]
            else:
                converted_data[block_address + local_position] = image_data[output_offset]
            output_offset += 1

    return converted_data


def unswizzle_psp(image_data: bytes, img_width: int, img_height: int, bpp: int) -> bytes:
    bytes_per_pixel = bpp // 8
    out_offset = 0
    stride: int = get_stride_value_psp(img_width, bpp)
    unswizzled_data: bytearray = _convert_psp(image_data, img_width, img_height, bpp, False)
    padded_data = bytearray(img_width * img_height * bytes_per_pixel)
    for y in range(img_height):
        row_start = y * stride
        row_end = row_start + img_width * bytes_per_pixel
        padded_data[out_offset: out_offset + img_width * bytes_per_pixel] = unswizzled_data[row_start: row_end]
        out_offset += img_width * bytes_per_pixel

    return padded_data


def swizzle_psp(image_data: bytes, img_width: int, img_height: int, bpp: int):
    bytes_per_pixel = bpp // 8
    stride = get_stride_value_psp(img_width, bpp)
    padded_data: bytearray = bytearray(stride * img_height)

    in_offset = 0
    for y in range(img_height):
        row_start = y * stride
        row_end = row_start + img_width * bytes_per_pixel
        padded_data[row_start:row_end] = image_data[in_offset: in_offset + img_width * bytes_per_pixel]
        in_offset += img_width * bytes_per_pixel

    return _convert_psp(padded_data, img_width, img_height, bpp, True)
