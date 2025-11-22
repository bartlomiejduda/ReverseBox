"""
Copyright © 2025 Bartłomiej Duda
License: GPL-3.0 License
"""

from reversebox.common.logger import get_logger

# from reversebox.io_files.bytes_helper_functions import get_bits, get_uint32

logger = get_logger(__name__)

# fmt: off

# EA IDEC (Image Decompression)
# https://rewiki.miraheze.org/wiki/EA_IDEC_Compression

# Used in *.SSH images in game "Theme Park World" (PS2)
# and probably in some other EA/Bullfrog games too


def decompress_ea_idec(image_data: bytes) -> bytes:
    if len(image_data) < 8 or image_data[:2] not in (b"MG", b"GM"):
        raise Exception("Data is not compressed with EA IDEC compression!")

    decompressed_data: bytearray = bytearray()

    # parse header
    # image_width: int = image_data[2] << 4
    # image_height: int = image_data[3] << 4
    # value1: int = get_uint32(image_data[4:8], "<")
    # size: int = get_bits(value1, 20, 0)
    # alpha_type: int = get_bits(value1, 2, 20)
    # alpha_quant: int = get_bits(value1, 5, 22)
    # flags: int = get_bits(value1, 5, 27)

    # TODO - implement logic

    return bytes(decompressed_data)
