"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

from reversebox.image.common import convert_bpp_to_bytes_per_pixel

# Morton Order Texture Swizzling (+ rotated by 90 degrees for Dreamcast CPU)
# https://en.wikipedia.org/wiki/Z-order_curve
# https://dreamcast.wiki/Twiddling
# Used in Dreamcast games

# fmt: off


def calculate_morton_index_dreamcast(p: int, w: int, h: int) -> int:
    ddx = 1
    ddy = w
    q = 0

    for i in range(16):
        h >>= 1
        if h:
            if p & 1:
                q |= ddy
            p >>= 1
        ddy <<= 1
        if w >> 1:
            if p & 1:
                q |= ddx
            p >>= 1
        ddx <<= 1

    return q


def _convert_morton_dreamcast(image_data: bytes, img_width: int, img_height: int, bpp: int, swizzle_flag: bool) -> bytes:
    converted_data = bytearray(len(image_data))
    bytes_per_pixel: int = convert_bpp_to_bytes_per_pixel(bpp)
    source_index: int = 0

    for t in range(img_width * img_height):
        index = calculate_morton_index_dreamcast(t, img_width, img_height)
        destination_index = bytes_per_pixel * index

        if not swizzle_flag:
            converted_data[destination_index: destination_index + bytes_per_pixel] = image_data[source_index: source_index + bytes_per_pixel]
        else:
            converted_data[source_index: source_index + bytes_per_pixel] = image_data[destination_index: destination_index + bytes_per_pixel]
        source_index += bytes_per_pixel

    return converted_data


def _convert_morton_dreamcast_4bit(input_buffer: bytes, width: int, height: int, bpp: int, swizzle_flag: bool) -> bytes:
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
    output_pixels_8bpp = _convert_morton_dreamcast(input_pixels_8bpp, width, height, bpp, swizzle_flag)

    # repack 8bpp pixels to 4bpp
    for i in range(buffer_byte_size):
        nybble_low = output_pixels_8bpp[i * 2]
        nybble_high = output_pixels_8bpp[i * 2 + 1]
        byte_value = (nybble_high << 4) | nybble_low
        converted_data[i] = byte_value

    return converted_data


def unswizzle_morton_dreamcast(image_data: bytes, img_width: int, img_height: int, bpp: int) -> bytes:
    if bpp == 4:
        return _convert_morton_dreamcast_4bit(image_data, img_width, img_height, bpp, False)
    return _convert_morton_dreamcast(image_data, img_width, img_height, bpp, False)


def swizzle_morton_dreamcast(image_data: bytes, img_width: int, img_height: int, bpp: int) -> bytes:
    if bpp == 4:
        return _convert_morton_dreamcast_4bit(image_data, img_width, img_height, bpp, True)
    return _convert_morton_dreamcast(image_data, img_width, img_height, bpp, True)
