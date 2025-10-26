"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

from reversebox.common.logger import get_logger

logger = get_logger(__name__)

# fmt: off

# TGA RLE compression (reversed condition)
# https://en.wikipedia.org/wiki/Truevision_TGA
# https://www.dca.fee.unicamp.br/~martino/disciplinas/ea978/tgaffs.pdf

# Used in Leapster PEG Bitmaps


def decompress_rle_tga_reversed(image_data: bytes, bpp: int) -> bytes:
    bytes_per_pixel = bpp // 8
    decompressed_data: list[int] = []
    i = 0

    while i < len(image_data):
        header = image_data[i]
        i += 1

        packet_type = header & 0x80
        count = (header & 0x7F) + 1

        if not packet_type:  # repeated packet
            pixel_data = image_data[i:i + bytes_per_pixel]
            i += bytes_per_pixel
            decompressed_data.extend(pixel_data * count)
        else:  # raw packet
            pixel_data = image_data[i:i + count * bytes_per_pixel]
            i += count * bytes_per_pixel
            decompressed_data.extend(pixel_data)

    return bytes(decompressed_data)
