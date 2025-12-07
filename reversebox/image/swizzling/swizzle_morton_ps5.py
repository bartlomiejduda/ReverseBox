"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

from reversebox.image.swizzling.morton_index import calculate_morton_index

# fmt: off

# Morton Order Texture Swizzling (+ extra PS5 swizzle logic)
# https://en.wikipedia.org/wiki/Z-order_curve
# Swizzle used in PS5 games


def _get_block_value(block_data_size: int) -> int:
    if block_data_size == 4:
        return 4
    elif block_data_size == 8:
        return 2
    else:
        return 1


def _convert_morton_ps5(image_data: bytes, img_width: int, img_height: int, block_width: int,
                        block_height: int, block_data_size: int, swizzle_flag: bool) -> bytes:
    converted_data = bytearray(len(image_data))
    source_index: int = 0
    img_height //= block_height
    img_width //= block_width

    if block_width == 1 and block_height == 1:
        for y in range((img_height + 127) // 128):
            for x in range((img_width + 127) // 128):
                for t in range(512):
                    morton_index = calculate_morton_index(t, 32, 16)
                    data_x: int = morton_index % 32
                    data_y: int = morton_index // 32
                    for i in range(32):
                        local_x: int = x * 128 + data_x * 4 + i % 4
                        local_y: int = y * 128 + (data_y * 8 + i // 4)
                        if local_x < img_width and local_y < img_height:
                            destination_index: int = block_data_size * (local_y * img_width + local_x)
                            if not swizzle_flag:
                                converted_data[destination_index: destination_index + block_data_size] = image_data[source_index: source_index + block_data_size]
                            else:
                                converted_data[source_index: source_index + block_data_size] = image_data[destination_index: destination_index + block_data_size]
                            source_index += block_data_size
    else:
        block_value: int = _get_block_value(block_data_size)
        for y in range((img_height + 63) // 64):
            for x in range((img_width + 63) // 64):
                for t in range(256 // block_value):
                    morton_index = calculate_morton_index(t, 16, 16 // block_value)
                    data_x: int = morton_index // 16
                    data_y: int = morton_index % 16
                    for i in range(16):
                        for j in range(block_value):
                            local_x: int = x * 64 + (data_x * 4 + i // 4) * block_value + j
                            local_y: int = y * 64 + data_y * 4 + i % 4
                            if local_x < img_width and local_y < img_height:
                                destination_index: int = block_data_size * (local_y * img_width + local_x)
                                if not swizzle_flag:
                                    converted_data[destination_index: destination_index + block_data_size] = image_data[source_index: source_index + block_data_size]
                                else:
                                    converted_data[source_index: source_index + block_data_size] = image_data[destination_index: destination_index + block_data_size]
                                source_index += block_data_size

    return converted_data


def unswizzle_ps5(image_data: bytes, img_width: int, img_height: int, block_width: int = 4, block_height: int = 4, block_data_size: int = 16) -> bytes:
    return _convert_morton_ps5(image_data, img_width, img_height, block_width, block_height, block_data_size, False)


def swizzle_ps5(image_data: bytes, img_width: int, img_height: int, block_width: int = 4, block_height: int = 4, block_data_size: int = 16) -> bytes:
    return _convert_morton_ps5(image_data, img_width, img_height, block_width, block_height, block_data_size, True)
