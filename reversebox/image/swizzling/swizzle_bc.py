"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

# BC Swizzle
# Used in some WII games like Mario Kart Wii

# fmt: off


def get_storage_wh(image_width: int, image_height: int, block_width: int, block_height: int) -> tuple:
    image_width = (image_width + block_width - 1) // block_width * block_width
    image_height = (image_height + block_height - 1) // block_height * block_height
    return image_width, image_height


def unswizzle_bc(image_data: bytes, image_width: int, image_height: int, block_width: int, block_height: int, bpp: int) -> bytes:
    strip_size: int = bpp * block_width // 8
    _width, _height = get_storage_wh(image_width, image_height, block_width, block_height)
    unswizzled_image_data = bytearray(_width * _height * bpp // 8)
    ptr: int = 0

    for y in range(0, _height, block_height):
        for x in range(0, _width, block_width):
            for y2 in range(block_height):
                idx = (((y + y2) * _width) + x) * bpp // 8
                unswizzled_image_data[idx: idx + strip_size] = image_data[ptr: ptr + strip_size]
                ptr += strip_size

    return unswizzled_image_data
