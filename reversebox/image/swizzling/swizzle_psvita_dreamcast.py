"""
Copyright © 2024-2025  Bartłomiej Duda
License: GPL-3.0 License
"""

from reversebox.image.common import convert_bpp_to_bytes_per_pixel

# fmt: off

# Dreamcast and PS Vita Texture Swizzling
# Morton Order (+ rotate by 90 degrees)
# https://en.wikipedia.org/wiki/Z-order_curve
# https://dreamcast.wiki/Twiddling

# Swizzling modes:
# block_width_height=1 --> linear formats
# block_width_height=4 --> BC formats, 4x4 blocks
# block_width_height=8 --> BC formats, 8x8 blocks

# Same algorithm is used in Dreamcast and PS Vita consoles
# I've seen it used in Dreamcast DTEX files and in PS Vita GXT files
# example games:
# - Danganronpa: Trigger Happy Havoc (PS Vita) (*.GXT)
# - Danganronpa 2: Goodbye Despair (PS Vita) (*.GXT)
# - Senran Kagura: Shinovi Versus (PS Vita) (*.GXT)


def calculate_morton_index_psvita_dreamcast(p: int, width: int, height: int) -> int:
    ddx = 1
    ddy = width
    q = 0

    for i in range(16):
        height >>= 1
        if height:
            if p & 1:
                q |= ddy
            p >>= 1
        ddy <<= 1
        if width >> 1:
            if p & 1:
                q |= ddx
            p >>= 1
        ddx <<= 1

    return q


def _convert_morton_psvita_dreamcast(pixel_data: bytes, img_width: int, img_height: int, bpp: int, block_width_height, swizzle_flag: bool) -> bytes:
    bytes_per_pixel: int = convert_bpp_to_bytes_per_pixel(bpp)
    block_data_size: int = bytes_per_pixel * block_width_height * block_width_height
    converted_data: bytearray = bytearray(len(pixel_data))
    img_height //= block_width_height
    img_width //= block_width_height
    source_index: int = 0

    for t in range(img_width * img_height):
        index = calculate_morton_index_psvita_dreamcast(t, img_width, img_height)
        destination_index = block_data_size * index
        if not swizzle_flag:
            converted_data[destination_index:destination_index + block_data_size] = pixel_data[source_index:source_index + block_data_size]
        else:
            converted_data[source_index:source_index + block_data_size] = pixel_data[destination_index:destination_index + block_data_size]
        source_index += block_data_size

    return converted_data


def unswizzle_psvita_dreamcast(pixel_data: bytes, img_width: int, img_height: int, bpp: int, block_width_height: int = 1) -> bytes:
    return _convert_morton_psvita_dreamcast(pixel_data, img_width, img_height, bpp, block_width_height, False)


def swizzle_psvita_dreamcast(pixel_data: bytes, img_width: int, img_height: int, bpp: int, block_width_height: int = 1) -> bytes:
    return _convert_morton_psvita_dreamcast(pixel_data, img_width, img_height, bpp, block_width_height, True)
