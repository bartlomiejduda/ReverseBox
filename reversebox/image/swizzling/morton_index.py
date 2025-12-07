"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

# fmt: off

# Helper function for calculating morton index


def calculate_morton_index(t: int, input_width: int, input_height: int) -> int:
    num1 = num2 = 1
    num3 = num4 = 0
    img_width: int = input_width
    img_height: int = input_height
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
    return num4 * input_width + num3
