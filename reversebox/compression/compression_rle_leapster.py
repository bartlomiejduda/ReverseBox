"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

from reversebox.common.logger import get_logger
from reversebox.image.common import convert_bpp_to_bytes_per_pixel
from reversebox.io_files.bytes_helper_functions import get_uint8

logger = get_logger(__name__)

# fmt: off

# WayForward's Leapster RLE Compression
# Used in many Leapster games like:
# - Cosmic Math
# - Letterpillar
# - Number Raiders
# - Word Chasers
# - The Batman: Strength in Numbers/Multiply, Divide and Conquer


def decompress_rle_leapster(image_data: bytes, image_width: int, image_height: int, bpp: int) -> bytes:
    if bpp not in (8, 16):
        raise Exception(f"Not supported bpp! Bpp={bpp}")

    bytes_per_pixel: int = convert_bpp_to_bytes_per_pixel(bpp)
    decompressed_data: bytearray = bytearray()
    input_offset: int = 0
    pixel_count: int = 0

    while pixel_count <= image_width * image_height:
        current_width: int = 0
        transparent_values_count: int = get_uint8(image_data[input_offset:input_offset + 1], "<")
        input_offset += 1
        color_values_count: int = get_uint8(image_data[input_offset:input_offset + 1], "<")
        input_offset += 1

        for _ in range(transparent_values_count):
            decompressed_data += int(0xF0).to_bytes(bytes_per_pixel, 'little')
            current_width += 1
            pixel_count += 1

        for _ in range(color_values_count):
            decompressed_data += image_data[input_offset:input_offset + bytes_per_pixel]
            input_offset += bytes_per_pixel
            current_width += 1
            pixel_count += 1

        for _ in range(image_width - current_width):
            decompressed_data += int(0xF0).to_bytes(bytes_per_pixel, 'little')
            pixel_count += 1

    return bytes(decompressed_data)
