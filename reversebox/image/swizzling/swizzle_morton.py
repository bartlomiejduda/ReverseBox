"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

from reversebox.image.common import convert_bpp_to_bytes_per_pixel

# Morton Order Texture Swizzling
# https://en.wikipedia.org/wiki/Z-order_curve
# Used in XBOX CLASSIC and PS3 games

# fmt: off


def calculate_morton_index(t: int, input_img_width: int, input_img_height: int) -> int:
    num1 = num2 = 1
    num3 = num4 = 0
    img_width: int = input_img_width
    img_height: int = input_img_height
    while img_width > 1 or img_height > 1:
        if img_width > 1:
            num3 += num2 * (t & 1)
            t >>= 1
            num2 *= 2
            img_width >>= 1
        if img_height > 1:
            num4 += num1 * (t & 1)
            t >>= 1
            num1 *= 2
            img_height >>= 1
    return num4 * input_img_width + num3


def unswizzle_morton(image_data: bytes, img_width: int, img_height: int, bpp: int) -> bytes:
    unswizzled_data = bytearray(len(image_data))
    bytes_per_pixel: int = convert_bpp_to_bytes_per_pixel(bpp)
    source_index: int = 0

    for t in range(img_width * img_height):
        index = calculate_morton_index(t, img_width, img_height)
        destination_index = bytes_per_pixel * index
        unswizzled_data[destination_index: destination_index + bytes_per_pixel] = image_data[source_index: source_index + bytes_per_pixel]
        source_index += bytes_per_pixel

    return unswizzled_data
