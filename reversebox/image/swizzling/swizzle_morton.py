"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

from reversebox.image.common import convert_bpp_to_bytes_per_pixel

# Morton Order Texture Swizzling
# https://en.wikipedia.org/wiki/Z-order_curve
# Used in XBOX CLASSIC and PS3 games (e.g. EA XSH files)

# fmt: off


def calculate_morton_index(x: int, y: int, img_width: int, img_height: int) -> int:
    nx: int = 0
    ny: int = 0
    xpos: int = 0
    ypos: int = 0
    tpix: int = 1
    morton_index: int = y * img_width + x

    while tpix < img_width or tpix < img_height:
        if tpix < img_width:
            nx |= ((morton_index & 1) << xpos)
            xpos += 1
            morton_index >>= 1
        if tpix < img_height:
            ny |= ((morton_index & 1) << ypos)
            ypos += 1
            morton_index >>= 1
        tpix <<= 1

    morton_index = ny * img_width + nx
    return morton_index


def unswizzle_morton(image_data: bytes, img_width: int, img_height: int, bpp: int) -> bytes:
    unswizzled_data = bytearray(len(image_data))
    bytes_per_pixel: int = convert_bpp_to_bytes_per_pixel(bpp)
    source_index: int = 0

    for y in range(img_height):
        for x in range(img_width):
            morton_index = calculate_morton_index(x, y, img_width, img_height)
            destination_index = bytes_per_pixel * morton_index
            unswizzled_data[destination_index: destination_index + bytes_per_pixel] = image_data[source_index: source_index + bytes_per_pixel]
            source_index += bytes_per_pixel

    return unswizzled_data


# TODO - not working as expected
def swizzle_morton(image_data: bytes, img_width: int, img_height: int, bpp: int) -> bytes:
    swizzled_data = bytearray(len(image_data))
    bytes_per_pixel: int = convert_bpp_to_bytes_per_pixel(bpp)
    source_index: int = 0

    for y in range(img_height):
        for x in range(img_width):
            morton_index = calculate_morton_index(x, y, img_width, img_height)
            destination_index = bytes_per_pixel * morton_index
            swizzled_data[source_index: source_index + bytes_per_pixel] = image_data[destination_index: destination_index + bytes_per_pixel]
            source_index += bytes_per_pixel

    return swizzled_data
