"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

import ctypes
from ctypes import byref, c_char

from reversebox.common.common import get_dll_path
from reversebox.io_files.bytes_handler import BytesHandler

# fmt: off


# this function can both swizzle and unswizzle ps2 palette
# it supports 32bit and 16bit palettes
def _convert_ps2_palette(palette_data: bytes) -> bytes:
    converted_palette_data: bytes = b""
    palette_handler = BytesHandler(palette_data)
    bytes_per_palette_pixel: int = 4
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
                    palette_entry = palette_handler.get_bytes(
                        palette_offset, bytes_per_palette_pixel
                    )
                    converted_palette_data += palette_entry

    return converted_palette_data


def unswizzle_ps2_palette(palette_data: bytes) -> bytes:
    return _convert_ps2_palette(palette_data)


def swizzle_ps2_palette(palette_data: bytes) -> bytes:
    return _convert_ps2_palette(palette_data)


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


# this is so-called "type 2" 4-bit PS2 swizzle function
# there is also "type 1" function which is not supported at the moment
# and "type 3" exist which is used for SSH files in EA games
def _convert_ps2_4bit_type2(input_buffer: bytes, width: int, height: int, swizzle_flag: bool) -> bytes:
    converted_data: bytearray = bytearray(len(input_buffer))
    input_pixels_8bpp = bytearray(width * height)
    buffer_byte_size = (width * height + 1) // 2

    # unpack 4bpp pixels to 8bpp
    for i in range(buffer_byte_size):
        byte_value = input_buffer[i]
        nybble_low = byte_value & 0xF
        nybble_high = byte_value >> 4
        input_pixels_8bpp[i * 2] = nybble_low
        input_pixels_8bpp[i * 2 + 1] = nybble_high

    # swizzle/unswizzle for 8bpp
    output_pixels_8bpp = _convert_ps2_8bit(input_pixels_8bpp, width, height, swizzle_flag)

    # repack 8bpp pixels to 4bpp
    for i in range(buffer_byte_size):
        nybble_low = output_pixels_8bpp[i * 2]
        nybble_high = output_pixels_8bpp[i * 2 + 1]
        byte_value = (nybble_high << 4) | nybble_low
        converted_data[i] = byte_value

    return converted_data


def _pixel16_offset(x: int, y: int, width: int) -> int:
    bit: int = 0

    if width >= 16:
        pagex = x >> 6
        pagey = y >> 6
        newx = (y & 0x38) + (x & 0x07)
        newy = ((x & 0x30) >> 1) + (y & 0x07)
        bit = ((x & 0x08) << 1)
        x = (pagex << 6) + newx
        y = (pagey << 5) + newy

    return 32 * (y * width + x) + bit


def _convert_ps2_16bit(image_data: bytes, width: int, height: int, swizzle_flag: bool) -> bytes:
    converted_data: bytearray = bytearray(len(image_data))

    for y in range(height):
        ywidth = y * width << 1
        for x in range(width):
            loc = _pixel16_offset(x, y, width) >> 3

            if not swizzle_flag:  # do unswizzle
                converted_data[(x << 1) + ywidth:(x << 1) + ywidth + 2] = image_data[loc:loc + 2]
            else:  # do swizzle
                converted_data[loc:loc + 2] = image_data[(x << 1) + ywidth:(x << 1) + ywidth + 2]

    return converted_data


# special "type 3" 4-bit swizzle/unswizzle function used in SSH files from EA PS2 games
def _convert_ps2_ea_4bit(image_data: bytes, img_width: int, img_height: int, bpp: int, swizzle_flag: bool) -> bytes:
    if bpp != 4:
        raise Exception(f"Not supported bpp={bpp} for EA swizzle!")

    converted_data_size: int = len(image_data)
    converted_data_buffer = (c_char * converted_data_size)()

    try:
        ea_swizzle_dll_path: str = get_dll_path("ea_swizzle.dll")
        ea_swizzle_dll_file = ctypes.CDLL(ea_swizzle_dll_path)
        if not swizzle_flag:
            ea_swizzle_dll_file.unswizzle4(image_data, byref(converted_data_buffer), img_width, img_height)
        else:
            ea_swizzle_dll_file.swizzle4(image_data, byref(converted_data_buffer), img_width, img_height)
    except Exception as error:
        raise Exception(f"Error while unswizzling data! Error: {error}")

    return bytes(bytearray(converted_data_buffer)[:converted_data_size])


def unswizzle_ps2_ea_4bit(image_data: bytes, img_width: int, img_height: int, bpp: int) -> bytes:
    return _convert_ps2_ea_4bit(image_data, img_width, img_height, bpp, False)


def swizzle_ps2_ea_4bit(image_data: bytes, img_width: int, img_height: int, bpp: int) -> bytes:
    return _convert_ps2_ea_4bit(image_data, img_width, img_height, bpp, True)


def unswizzle_ps2(image_data: bytes, img_width: int, img_height: int, bpp: int) -> bytes:
    if bpp == 4:
        return _convert_ps2_4bit_type2(image_data, img_width, img_height, False)
    elif bpp == 8:
        return _convert_ps2_8bit(image_data, img_width, img_height, False)
    elif bpp in (15, 16):
        return _convert_ps2_16bit(image_data, img_width, img_height, False)
    else:
        raise Exception(f"Bpp {bpp} not supported for PS2 unswizzle!")


def swizzle_ps2(image_data: bytes, img_width: int, img_height: int, bpp: int) -> bytes:
    if bpp == 4:
        return _convert_ps2_4bit_type2(image_data, img_width, img_height, True)
    elif bpp == 8:
        return _convert_ps2_8bit(image_data, img_width, img_height, True)
    elif bpp in (15, 16):
        return _convert_ps2_16bit(image_data, img_width, img_height, True)
    else:
        raise Exception(f"Bpp {bpp} not supported for PS2 swizzle!")

# fmt: on
