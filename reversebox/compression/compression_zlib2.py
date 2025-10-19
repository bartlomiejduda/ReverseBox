"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

import zlib

from reversebox.common.logger import get_logger

logger = get_logger(__name__)

# fmt: off

# ZLIB (deflate) compression
# Used in TIFF files


def decompress_zlib(image_data: bytes) -> bytes:
    try:
        decompress = zlib.decompressobj(wbits=zlib.MAX_WBITS)
        decompressed_data: bytes = decompress.decompress(image_data)
        decompressed_data += decompress.flush()
        return decompressed_data
    except Exception as error:
        logger.error(f"Error while decompressing ZLIB data. Error: {error}")
        return image_data


def compress_zlib(image_data: bytes, compress_level: int = 9) -> bytes:
    compress = zlib.compressobj(
            level=compress_level,
            method=zlib.DEFLATED,
            wbits=zlib.MAX_WBITS,
            memLevel=zlib.DEF_MEM_LEVEL,
            strategy=0
    )
    compressed_data = compress.compress(image_data)
    compressed_data += compress.flush()
    return compressed_data
