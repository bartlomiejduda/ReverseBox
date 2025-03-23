"""
Copyright © 2024-2025  Bartłomiej Duda
License: GPL-3.0 License
"""

from reversebox.image.common import convert_bpp_to_bytes_per_pixel

# Morton Order Texture Swizzling
# https://en.wikipedia.org/wiki/Z-order_curve
# Used in XBOX CLASSIC and PS3 games (e.g. EA XSH files)

# Swizzling modes:
# block_width_height=1 --> linear formats
# block_width_height=4 --> BC formats, 4x4 blocks
# block_width_height=8 --> BC formats, 8x8 blocks

# fmt: off


def calculate_morton_index(t: int, width: int, height: int) -> int:
    num1 = num2 = 1
    num3 = t
    t_width = width
    t_height = height
    num6 = num7 = 0

    while t_width > 1 or t_height > 1:
        if t_width > 1:
            num6 += num2 * (num3 & 1)
            num3 >>= 1
            num2 *= 2
            t_width >>= 1
        if t_height > 1:
            num7 += num1 * (num3 & 1)
            num3 >>= 1
            num1 *= 2
            t_height >>= 1

    return num7 * width + num6


def _convert_morton(pixel_data: bytes, img_width: int, img_height: int, bpp: int, block_width_height, swizzle_flag: bool) -> bytes:
    bytes_per_pixel: int = convert_bpp_to_bytes_per_pixel(bpp)
    block_data_size: int = bytes_per_pixel * block_width_height * block_width_height
    converted_data: bytearray = bytearray(len(pixel_data))
    img_height //= block_width_height
    img_width //= block_width_height
    source_index: int = 0

    for t in range(img_width * img_height):
        index = calculate_morton_index(t, img_width, img_height)
        destination_index = block_data_size * index
        if not swizzle_flag:
            converted_data[destination_index:destination_index + block_data_size] = pixel_data[source_index:source_index + block_data_size]
        else:
            converted_data[source_index:source_index + block_data_size] = pixel_data[destination_index:destination_index + block_data_size]
        source_index += block_data_size

    return converted_data


def unswizzle_morton(pixel_data: bytes, img_width: int, img_height: int, bpp: int, block_width_height: int = 1) -> bytes:
    return _convert_morton(pixel_data, img_width, img_height, bpp, block_width_height, False)


def swizzle_morton(pixel_data: bytes, img_width: int, img_height: int, bpp: int, block_width_height: int = 1) -> bytes:
    return _convert_morton(pixel_data, img_width, img_height, bpp, block_width_height, True)
