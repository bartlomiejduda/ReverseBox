"""
Copyright © 2026  Bartłomiej Duda
License: GPL-3.0 License
"""

from reversebox.common.logger import get_logger

logger = get_logger(__name__)

# fmt: off

# Syberia RLE compression
# https://rewiki.miraheze.org/wiki/Microids_VRLE


# TODO - implement this
def decompress_rle_syberia(image_data: bytes, img_width: int, img_height: int) -> bytes:
    return bytes(image_data)
