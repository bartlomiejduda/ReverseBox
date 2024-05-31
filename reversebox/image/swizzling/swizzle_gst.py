"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

import struct

# PS2 GS texture swizzling


def get_base_offset(
    x: int, y: int, width: int, block_width: int, block_height: int
) -> int:
    x *= block_width
    y *= block_height
    x1 = ((x & ~0x0F) >> 1) + ((x & 0x07) ^ ((y & 0x02) << 1) ^ (y & 0x04))
    y1 = ((y & ~0x03) >> 1) + (y & 0x01)
    z1 = ((x & 0x08) >> 2) + ((y & 0x02) >> 1)
    x1 //= block_width
    y1 //= block_height
    return 32 * (y1 * width // 2 + x1) + 8 * z1


def get_detail1_offset(x: int, y: int, width: int) -> int:
    x1 = ((x & ~0x0F) >> 1) + ((x & 0x07) ^ ((y & 0x02) << 1) ^ (y & 0x04))
    y1 = ((y & ~0x03) >> 1) + (y & 0x01)
    z1 = ((x & 0x08) >> 2) + ((y & 0x02) >> 1)
    x2 = ((x1 & ~0x0F) >> 1) + ((x1 & 0x07) ^ ((y1 & 0x02) << 1) ^ (y1 & 0x04))
    y2 = ((y1 & ~0x03) >> 1) + (y1 & 0x01)
    z2 = ((x1 & 0x08) >> 2) + ((y1 & 0x02) >> 1)
    return 16 * (y2 * width // 4 + x2) + 4 * z2 + z1


def get_detail2_offset(x: int, y: int, width: int) -> int:
    x1 = ((x & ~0x0F) >> 1) + ((x & 0x07) ^ ((y & 0x02) << 1) ^ (y & 0x04))
    y1 = ((y & ~0x03) >> 1) + (y & 0x01)
    z1 = ((x & 0x08) >> 2) + ((y & 0x02) >> 1)
    x2 = ((x1 & ~0x0F) >> 1) + ((x1 & 0x07) ^ ((y1 & 0x02) << 1) ^ (y1 & 0x04))
    y2 = ((y1 & ~0x03) >> 1) + (y1 & 0x01)
    z2 = ((x1 & 0x08) >> 2) + ((y1 & 0x02) >> 1)
    return 32 * (y2 * width // 4 + x2) + 8 * z2 + 2 * z1


def get_1_bit(input_bytes: bytes, offset: int) -> int:
    index = offset >> 3
    bit = offset & 0x07
    return input_bytes[index] >> bit & 1


def get_2_bits(input_bytes: bytes, offset: int) -> int:
    index = offset >> 3
    bit = offset & 0x07
    return input_bytes[index] >> bit & 3


def unswizzle_gst_base(
    image_data: bytes,
    img_width: int,
    img_height: int,
    block_width: int,
    block_height: int,
) -> bytes:
    base_width = img_width // block_width
    base_height = img_height // block_height
    unswizzled_data: bytes = b""

    for y in range(base_height):
        for x in range(base_width):
            offset = get_base_offset(x, y, base_width, block_width, block_height)
            data_byte = image_data[offset >> 3] & 0xFF
            unswizzled_data += struct.pack("B", data_byte)

    return unswizzled_data


def unswizzle_detail1(image_data: bytes, img_width: int, img_height: int) -> bytes:
    unswizzled_data: bytes = b""
    for y in range(img_height):
        for x in range(0, img_width, 8):
            data_byte = 0
            x_final = 7
            while x_final >= 0:
                offset = get_detail1_offset(x + x_final, y, img_width)
                data_byte = (data_byte << 1) + get_1_bit(image_data, offset)
                x_final -= 1
            unswizzled_data += struct.pack("B", data_byte)

    return unswizzled_data


def unswizzle_detail2(image_data: bytes, img_width: int, img_height: int) -> bytes:
    unswizzled_data: bytes = b""
    for y in range(img_height):
        for x in range(0, img_width, 4):
            data_byte = 0
            x_final = 3
            while x_final >= 0:
                offset = get_detail2_offset(x + x_final, y, img_width)
                data_byte = (data_byte << 2) + get_2_bits(image_data, offset)
                x_final -= 1
            unswizzled_data += struct.pack("B", data_byte)

    return unswizzled_data
