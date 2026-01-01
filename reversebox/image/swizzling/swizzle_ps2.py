"""
Copyright © 2024-2025  Bartłomiej Duda
License: GPL-3.0 License
"""

from reversebox.image.swizzling.swizzle_ps2_4bit import _ps2_swizzle4, _ps2_unswizzle4
from reversebox.io_files.bytes_handler import BytesHandler

# fmt: off

# PS2 Swizzle


# this function can both swizzle and unswizzle PS2 palette
# converts from CSM1 to CSM2 and from CSM2 to CSM1
# it supports 32bit and 16bit palettes
def _convert_ps2_palette(palette_data: bytes, bpp: int = 32) -> bytes:
    if bpp == 32:
        bytes_per_palette_pixel: int = 4
    elif bpp == 16:
        bytes_per_palette_pixel: int = 2
    else:
        raise ValueError(f"Bpp {bpp} not supported!")

    converted_palette_data: bytes = b""
    palette_handler = BytesHandler(palette_data)

    parts: int = int(len(palette_data) / 32)
    stripes: int = 2
    colors: int = 8
    blocks: int = 2
    index: int = 0

    for part in range(parts):
        for block in range(blocks):
            for stripe in range(stripes):
                for color in range(colors):
                    palette_index: int = (
                        index
                        + part * colors * stripes * blocks
                        + block * colors
                        + stripe * stripes * colors
                        + color
                    )
                    palette_offset: int = palette_index * bytes_per_palette_pixel
                    palette_entry = palette_handler.get_bytes(palette_offset, bytes_per_palette_pixel)
                    converted_palette_data += palette_entry

    return converted_palette_data


def unswizzle_ps2_palette(palette_data: bytes) -> bytes:
    return _convert_ps2_palette(palette_data)


def swizzle_ps2_palette(palette_data: bytes) -> bytes:
    return _convert_ps2_palette(palette_data)


# 8bpp TYPE 1/2
def _convert_ps2_8bit(image_data: bytes, img_width: int, img_height: int, swizzle_flag: bool) -> bytes:
    converted_data: bytearray = bytearray(img_width * img_height)
    for y in range(img_height):
        for x in range(img_width):
            block_location = (y & (~0xF)) * img_width + (x & (~0xF)) * 2
            swap_selector = (((y + 2) >> 2) & 0x1) * 4
            pos_y = (((y & (~3)) >> 1) + (y & 1)) & 0x7
            column_location = pos_y * img_width * 2 + ((x + swap_selector) & 0x7) * 4
            byte_num = ((y >> 1) & 1) + ((x >> 2) & 2)
            swizzle_id = block_location + column_location + byte_num

            if not swizzle_flag:  # do unswizzle
                converted_data[y * img_width + x] = image_data[swizzle_id]
            else:  # do swizzle
                converted_data[swizzle_id] = image_data[y * img_width + x]

    return converted_data


def _pixel16_offset(x: int, y: int, width: int) -> int:
    bit: int = 0

    if width >= 16:
        pagex = x >> 6
        pagey = y >> 6
        newx = (y & 0x38) + (x & 0x07)
        newy = ((x & 0x30) >> 1) + (y & 0x07)
        bit = (x & 0x08) << 1
        x = (pagex << 6) + newx
        y = (pagey << 5) + newy

    return 32 * (y * width + x) + bit


# 16-bpp TYPE 1/2
# TODO - fix this, not unswizzling correctly
def _convert_ps2_16bit(image_data: bytes, width: int, height: int, swizzle_flag: bool) -> bytes:
    converted_data: bytearray = bytearray(len(image_data))

    for y in range(height):
        ywidth = y * width << 1
        for x in range(width):
            loc = _pixel16_offset(x, y, width) >> 3
            dest_index = (x << 1) + ywidth

            if not swizzle_flag:  # do unswizzle
                converted_data[dest_index: dest_index + 2] = image_data[loc:loc + 2]
            else:  # do swizzle
                converted_data[loc:loc + 2] = image_data[dest_index: dest_index + 2]

    return converted_data


# 4-bpp TYPE 1
# used in EA games
def _convert_ps2_4bit_type1(image_data: bytes, img_width: int, img_height: int, swizzle_flag: bool) -> bytes:
    if not swizzle_flag:
        converted_data = _ps2_unswizzle4(image_data, img_width, img_height)
    else:
        converted_data = _ps2_swizzle4(image_data, img_width, img_height)

    return bytes(converted_data)


# 4-bpp TYPE 2
# used in Console Texture Explorer
def _convert_ps2_4bit_type2(image_data: bytes, img_width: int, img_height: int, swizzle_flag: bool) -> bytes:
    converted_data: bytearray = bytearray(len(image_data))
    input_pixels_8bpp = bytearray(img_width * img_height)
    buffer_byte_size = (img_width * img_height + 1) // 2

    # unpack 4bpp pixels to 8bpp
    for i in range(buffer_byte_size):
        byte_value = image_data[i]
        nybble_low = byte_value & 0xF
        nybble_high = byte_value >> 4
        input_pixels_8bpp[i * 2] = nybble_low
        input_pixels_8bpp[i * 2 + 1] = nybble_high

    # swizzle/unswizzle for 8bpp
    output_pixels_8bpp = _convert_ps2_8bit(input_pixels_8bpp, img_width, img_height, swizzle_flag)

    # repack 8bpp pixels to 4bpp
    for i in range(buffer_byte_size):
        nybble_low = output_pixels_8bpp[i * 2]
        nybble_high = output_pixels_8bpp[i * 2 + 1]
        byte_value = (nybble_high << 4) | nybble_low
        converted_data[i] = byte_value

    return converted_data


def unswizzle_ps2(image_data: bytes, img_width: int, img_height: int, bpp: int, swizzle_type: int = 1) -> bytes:
    if swizzle_type not in (1, 2):
        raise Exception(f"Not supported swizzle type {swizzle_type}!")

    if bpp == 4:
        if swizzle_type == 1:
            return _convert_ps2_4bit_type1(image_data, img_width, img_height, False)
        if swizzle_type == 2:
            return _convert_ps2_4bit_type2(image_data, img_width, img_height, False)
    elif bpp == 8:
        return _convert_ps2_8bit(image_data, img_width, img_height, False)
    elif bpp in (15, 16):
        return _convert_ps2_16bit(image_data, img_width, img_height, False)
    else:
        raise Exception(f"Bpp {bpp} not supported for PS2 unswizzle!")

    raise Exception("Data couldn't be unswizzled!")


def swizzle_ps2(image_data: bytes, img_width: int, img_height: int, bpp: int, swizzle_type: int = 1) -> bytes:
    if swizzle_type not in (1, 2):
        raise Exception(f"Not supported swizzle type {swizzle_type}!")

    if bpp == 4:
        if swizzle_type == 1:
            return _convert_ps2_4bit_type1(image_data, img_width, img_height, True)
        if swizzle_type == 2:
            return _convert_ps2_4bit_type2(image_data, img_width, img_height, True)
    elif bpp == 8:
        return _convert_ps2_8bit(image_data, img_width, img_height, True)
    elif bpp in (15, 16):
        return _convert_ps2_16bit(image_data, img_width, img_height, True)
    else:
        raise Exception(f"Bpp {bpp} not supported for PS2 swizzle!")

    raise Exception("Data couldn't be swizzled!")
