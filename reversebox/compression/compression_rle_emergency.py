"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

from reversebox.common.logger import get_logger

logger = get_logger(__name__)

# fmt: off

# RLE Emergency Compression
# Used in CFF image files from "Emergency: Fighters For Life"


def decompress_rle_emergency(image_data: bytes, image_width: int, image_height: int, bpp: int) -> bytes:
    if bpp != 8:
        raise Exception(f"Not supported bpp! Bpp={bpp}")

    compressed_data: bytearray = bytearray(image_data)
    output_size: int = image_width * image_height
    decompressed_data: bytearray = bytearray(output_size)
    input_offset: int = 0
    output_offset: int = 0

    while 1:
        control_byte = image_data[input_offset]

        if control_byte == 0:
            input_offset += 1
            break

        if output_offset >= output_size:
            break

        if control_byte & 0x80:  # repeated packet
            colour: int = compressed_data[input_offset + 1]
            input_offset += 2

            for i in range((control_byte & 0x7f) + 1):
                decompressed_data[output_offset + i] = colour

            output_offset += ((control_byte & 0x7f) + 1)
        else:  # raw packet
            decompressed_data[output_offset:output_offset + control_byte] = compressed_data[input_offset + 1: input_offset + 1 + control_byte]

            output_offset += control_byte
            input_offset += control_byte + 1

    return bytes(decompressed_data)
