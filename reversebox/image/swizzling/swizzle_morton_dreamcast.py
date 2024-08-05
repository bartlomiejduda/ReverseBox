"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

from reversebox.image.common import convert_bpp_to_bytes_per_pixel

# Morton Order Texture Swizzling (+ rotated by 90 degrees for Dreamcast CPU)
# https://en.wikipedia.org/wiki/Z-order_curve
# https://dreamcast.wiki/Twiddling
# Used in Dreamcast games

# fmt: off


def calculate_morton_index_dreamcast(p: int, w: int, h: int) -> int:
    ddx = 1
    ddy = w
    q = 0

    for i in range(16):
        if h >> 1:
            h >>= 1
            if p & 1:
                q |= ddy
            p >>= 1
        ddy <<= 1
        if w >> 1:
            if p & 1:
                q |= ddx
            p >>= 1
        ddx <<= 1

    return q


def unswizzle_morton_dreamcast(image_data: bytes, img_width: int, img_height: int, bpp: int) -> bytes:
    unswizzled_data = bytearray(len(image_data))
    bytes_per_pixel: int = convert_bpp_to_bytes_per_pixel(bpp)
    source_index: int = 0

    for t in range(img_width * img_height):
        index = calculate_morton_index_dreamcast(t, img_width, img_height)
        destination_index = bytes_per_pixel * index
        unswizzled_data[destination_index: destination_index + bytes_per_pixel] = image_data[source_index: source_index + bytes_per_pixel]
        source_index += bytes_per_pixel

    return unswizzled_data
