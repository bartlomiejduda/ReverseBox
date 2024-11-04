"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

# fmt: off

# Swizzle used in PS4 games e.g. "Dragons Dogma Dark Arisen" (MT Framework TEX files)


def calculate_morton_index_ps4(t: int, input_img_width: int, input_img_height: int) -> int:
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


def unswizzle_ps4(image_data: bytes, img_width: int, img_height: int, block_width: int = 4, block_height: int = 4, block_data_size: int = 16) -> bytes:
    unswizzled_data = bytearray(len(image_data))
    source_index: int = 0
    img_height //= block_height
    img_width //= block_width

    for y in range((img_height + 7) // 8):
        for x in range((img_width + 7) // 8):
            for t in range(64):
                morton_index = calculate_morton_index_ps4(t, 8, 8)
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
                morton_index = calculate_morton_index_ps4(t, 8, 8)
                data_y = morton_index // 8
                data_x = morton_index % 8
                if x * 8 + data_x < img_width and y * 8 + data_y < img_height:
                    destination_index = block_data_size * ((y * 8 + data_y) * img_width + x * 8 + data_x)
                    swizzled_data[source_index: source_index + block_data_size] = image_data[destination_index: destination_index + block_data_size]
                    source_index += block_data_size

    return swizzled_data
