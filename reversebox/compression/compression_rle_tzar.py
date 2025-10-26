"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

from typing import List

from reversebox.common.logger import get_logger
from reversebox.image.common import convert_bpp_to_bytes_per_pixel
from reversebox.io_files.bytes_helper_functions import get_uint8, get_uint32

logger = get_logger(__name__)

# fmt: off

# Tzar RLE Compression
# Used in *.RLE images in game "Tzar: The Burden of the Crown"


def decompress_rle_tzar(image_data: bytes, image_width: int, image_height: int, bpp: int) -> bytes:
    if bpp not in (8, 16):
        raise Exception(f"Not supported bpp! Bpp={bpp}")

    bytes_per_pixel: int = convert_bpp_to_bytes_per_pixel(bpp)
    decompressed_data: bytearray = bytearray()
    input_offset: int = 0

    row_offsets_list: List[int] = []
    for _ in range(image_height):
        row_offsets_list.append(get_uint32(image_data[input_offset:input_offset+4], "<"))
        input_offset += 4

    for row_offset in row_offsets_list:
        input_offset = row_offset
        row_data: bytearray = bytearray()

        while 1:
            if len(row_data) >= (image_width * bytes_per_pixel):
                break

            transparent_values_count: int = get_uint8(image_data[input_offset:input_offset+1], "<")
            input_offset += 1
            color_values_count: int = get_uint8(image_data[input_offset:input_offset+1], "<")
            input_offset += 1

            for _ in range(transparent_values_count):
                row_data += int(0x6F).to_bytes(bytes_per_pixel, 'little')

            for _ in range(color_values_count):
                row_data += image_data[input_offset:input_offset+bytes_per_pixel]
                input_offset += bytes_per_pixel

        decompressed_data += row_data

    return bytes(decompressed_data)
