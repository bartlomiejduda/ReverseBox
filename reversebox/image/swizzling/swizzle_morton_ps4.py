"""
Copyright © 2024-2025  Bartłomiej Duda
License: GPL-3.0 License
"""

from reversebox.image.swizzling.morton_index import calculate_morton_index

# fmt: off

# Morton Order Texture Swizzling (+ extra PS4 swizzle logic)
# https://en.wikipedia.org/wiki/Z-order_curve
# Swizzle used in PS4 games e.g. "Dragons Dogma Dark Arisen" (MT Framework TEX files)


def _convert_morton_ps4(image_data: bytes, img_width: int, img_height: int, block_width: int,
                        block_height: int, block_data_size: int, swizzle_flag: bool) -> bytes:
    converted_data = bytearray(len(image_data))
    source_index: int = 0
    img_height //= block_height
    img_width //= block_width

    for y in range((img_height + 7) // 8):
        for x in range((img_width + 7) // 8):
            for t in range(64):
                morton_index = calculate_morton_index(t, 8, 8)
                data_y = morton_index // 8
                data_x = morton_index % 8
                if x * 8 + data_x < img_width and y * 8 + data_y < img_height:
                    destination_index = block_data_size * ((y * 8 + data_y) * img_width + x * 8 + data_x)
                    if not swizzle_flag:
                        converted_data[destination_index: destination_index + block_data_size] = image_data[source_index: source_index + block_data_size]
                    else:
                        converted_data[source_index: source_index + block_data_size] = image_data[destination_index: destination_index + block_data_size]
                    source_index += block_data_size

    return converted_data


def unswizzle_ps4(image_data: bytes, img_width: int, img_height: int, block_width: int = 4, block_height: int = 4, block_data_size: int = 16) -> bytes:
    return _convert_morton_ps4(image_data, img_width, img_height, block_width, block_height, block_data_size, False)


def swizzle_ps4(image_data: bytes, img_width: int, img_height: int, block_width: int = 4, block_height: int = 4, block_data_size: int = 16) -> bytes:
    return _convert_morton_ps4(image_data, img_width, img_height, block_width, block_height, block_data_size, True)
