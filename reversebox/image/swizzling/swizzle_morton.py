"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

from reversebox.image.common import convert_bpp_to_bytes_per_pixel

# Morton Order Texture Swizzling
# Used in XBOX and PS3 games

# fmt: off


def calculate_morton_index(input_t: int, input_img_width: int, input_img_height: int) -> int:
    num2 = num1 = 1
    t = input_t
    img_width = input_img_width
    img_height = input_img_height
    num6 = 0
    num7 = 0
    while img_width > 1 or img_height > 1:
        if img_width > 1:
            num6 += num2 * (t & 1)
            t >>= 1
            num2 *= 2
            img_width >>= 1
        if img_height > 1:
            num7 += num1 * (t & 1)
            t >>= 1
            num1 *= 2
            img_height >>= 1
    return num7 * input_img_width + num6


def unswizzle_morton(image_data: bytes, img_width: int, img_height: int, bpp: int) -> bytes:
    unswizzled_data = bytearray(len(image_data))
    bytes_per_pixel: int = convert_bpp_to_bytes_per_pixel(bpp)
    source_index: int = 0

    for t in range(img_width * img_height):
        index = calculate_morton_index(t, img_width, img_height)
        destination_index = bytes_per_pixel * index
        unswizzled_data[destination_index: destination_index + 2] = image_data[source_index: source_index + bytes_per_pixel]
        source_index += bytes_per_pixel

    return unswizzled_data
