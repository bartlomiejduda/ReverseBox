"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

from reversebox.image.swizzling.morton_index import calculate_morton_index

# fmt: off

# Morton Order Texture Swizzling (+ extra PS4 swizzle logic)
# https://en.wikipedia.org/wiki/Z-order_curve
# Swizzle used in PS4 games e.g. "Dragons Dogma Dark Arisen" (MT Framework TEX files)


def unswizzle_ps4(image_data: bytes, img_width: int, img_height: int, block_width: int = 4, block_height: int = 4, block_data_size: int = 16) -> bytes:
    unswizzled_data = bytearray(len(image_data))
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
                    unswizzled_data[destination_index: destination_index + block_data_size] = image_data[source_index: source_index + block_data_size]
                    source_index += block_data_size

    return unswizzled_data


def swizzle_ps4(image_data: bytes, img_width: int, img_height: int, block_width: int = 4, block_height: int = 4, block_data_size: int = 16) -> bytes:
    swizzled_data = bytearray(len(image_data))
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
                    swizzled_data[source_index: source_index + block_data_size] = image_data[destination_index: destination_index + block_data_size]
                    source_index += block_data_size

    return swizzled_data
