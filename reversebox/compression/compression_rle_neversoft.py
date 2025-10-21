"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

from reversebox.common.logger import get_logger
from reversebox.io_files.bytes_helper_functions import get_uint16, set_uint16

logger = get_logger(__name__)

# fmt: off

# Neversoft RLE Compression
# Used in *.RLE images in games like "Spider-Man", "Spider-Man 2", "Apocalypse" etc.


def decompress_rle_neversoft(image_data: bytes, bpp: int) -> bytes:
    if bpp != 16:
        raise Exception(f"Not supported bpp! Bpp={bpp}")

    decompressed_data: bytearray = bytearray()
    input_offset: int = 0

    while 1:
        if input_offset >= len(image_data):
            break

        command: int = get_uint16(image_data[input_offset:input_offset+2], "<")
        input_offset += 2
        count = command & 0x7fff
        command = command >> 15

        if command == 0:  # raw packet
            for _ in range(count):
                decompressed_data += image_data[input_offset:input_offset+2]
                input_offset += 2
        if command == 1:  # repeated packet
            colour = get_uint16(image_data[input_offset:input_offset+2], "<")
            input_offset += 2
            for _ in range(count):
                decompressed_data += set_uint16(colour, "<")

    return bytes(decompressed_data)
