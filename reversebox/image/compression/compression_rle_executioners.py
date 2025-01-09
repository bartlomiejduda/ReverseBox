"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

from reversebox.common.logger import get_logger
from reversebox.image.common import convert_bpp_to_bytes_per_pixel

logger = get_logger(__name__)

# fmt: off

# Executioners RLE compression
# https://moddingwiki.shikadi.net/wiki/Executioners_RLE_Format
# very similar to TGA RLE
# used in "Executioners" DOS game in some graphics like "EDLAUGH.VOL", "GR3.VOL" etc.
# extracted from INTRO.VOL archive


def decompress_rle_executioners(image_data: bytes, img_width: int, img_height: int, bpp: int) -> bytes:
    bytes_per_pixel: int = convert_bpp_to_bytes_per_pixel(bpp)
    decompressed_data: bytearray = bytearray(img_width * img_height * bytes_per_pixel)
    for i in range(img_width * img_height * bytes_per_pixel):
        decompressed_data[i] = 0xFF

    read_pos: int = 0
    write_pos: int = 0
    while write_pos < (img_width * img_height * bytes_per_pixel):
        code = image_data[read_pos]
        read_pos += 1

        is_repeat = code & 0x80 != 0
        count = (code & 0x7F)

        if is_repeat:  # repeated packet
            write_pos += count * bytes_per_pixel
        else:  # raw packet
            decompressed_data[write_pos: write_pos + count * bytes_per_pixel] = image_data[read_pos:read_pos + count * bytes_per_pixel]
            read_pos += count * bytes_per_pixel
            write_pos += count * bytes_per_pixel

    return bytes(decompressed_data)
