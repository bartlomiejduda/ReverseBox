"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

# PS2 GS texture swizzling
# Used in some EA games like "Cricket 2007" (PS2) and "FIFA Street" (PS2)


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
    return 16 * (y2 * (width // 4) + x2) + 4 * z2 + z1


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
    return (input_bytes[index] >> bit) & 1


def set_1_bit(input_bytes: bytearray, offset: int, value: int) -> None:
    index = offset >> 3
    bit = offset & 0x07
    input_bytes[index] = (input_bytes[index] & ~(1 << bit)) | (value << bit)


def get_2_bits(input_bytes: bytes, offset: int) -> int:
    index = offset >> 3
    bit = offset & 0x07
    return (input_bytes[index] >> bit) & 3


def set_2_bits(input_bytes: bytearray, offset: int, value: int) -> None:
    index = offset >> 3
    bit = offset & 0x07
    input_bytes[index] = (input_bytes[index] & ~(3 << bit)) | (value << bit)


def _convert_gst_base(
    image_data: bytes,
    img_width: int,
    img_height: int,
    block_width: int,
    block_height: int,
    swizzle_flag: bool,
) -> bytes:
    base_width = img_width // block_width
    base_height = img_height // block_height
    converted_data: bytearray = bytearray(len(image_data))
    counter: int = 0

    for y in range(base_height):
        for x in range(base_width):
            offset = get_base_offset(x, y, base_width, block_width, block_height)
            if not swizzle_flag:
                converted_data[counter] = image_data[offset >> 3] & 0xFF
            else:
                converted_data[offset >> 3] = image_data[counter]
            counter += 1

    return converted_data


def unswizzle_gst_base(
    image_data: bytes,
    img_width: int,
    img_height: int,
    block_width: int,
    block_height: int,
) -> bytes:
    return _convert_gst_base(
        image_data, img_width, img_height, block_width, block_height, False
    )


def swizzle_gst_base(
    image_data: bytes,
    img_width: int,
    img_height: int,
    block_width: int,
    block_height: int,
) -> bytes:
    return _convert_gst_base(
        image_data, img_width, img_height, block_width, block_height, True
    )


def unswizzle_gst_detail1(image_data: bytes, img_width: int, img_height: int) -> bytes:
    unswizzled_data: bytearray = bytearray(len(image_data))
    dest_index: int = 0
    for y in range(img_height):
        for x in range(0, img_width, 8):
            data = 0
            for xfine in range(7, -1, -1):
                offset = get_detail1_offset(x + xfine, y, img_width)
                data = (data << 1) + get_1_bit(image_data, offset)
            unswizzled_data[dest_index] = data
            dest_index += 1

    return unswizzled_data


def swizzle_gst_detail1(image_data: bytes, img_width: int, img_height: int) -> bytes:
    swizzled_data: bytearray = bytearray(len(image_data))
    source_index: int = 0
    for y in range(img_height):
        for x in range(0, img_width, 8):
            data = image_data[source_index]
            for xfine in range(8):
                offset = get_detail1_offset(x + xfine, y, img_width)
                set_1_bit(swizzled_data, offset, data & 1)
                data >>= 1
            source_index += 1

    return swizzled_data


def unswizzle_gst_detail2(image_data: bytes, img_width: int, img_height: int) -> bytes:
    unswizzled_data: bytearray = bytearray(len(image_data))
    dest_index: int = 0
    for y in range(img_height):
        for x in range(0, img_width, 4):
            data_byte = 0
            x_final = 3
            while x_final >= 0:
                offset = get_detail2_offset(x + x_final, y, img_width)
                data_byte = (data_byte << 2) + get_2_bits(image_data, offset)
                x_final -= 1
            unswizzled_data[dest_index] = data_byte
            dest_index += 1

    return unswizzled_data


def swizzle_gst_detail2(image_data: bytes, img_width: int, img_height: int) -> bytes:
    swizzled_data: bytearray = bytearray(len(image_data))
    source_index: int = 0
    for y in range(img_height):
        for x in range(0, img_width, 4):
            data = image_data[source_index]
            for xfine in range(4):
                offset = get_detail2_offset(x + xfine, y, img_width)
                set_2_bits(swizzled_data, offset, data & 3)
                data >>= 2
            source_index += 1

    return swizzled_data
