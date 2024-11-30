"""
Copyright © 2022  Bartłomiej Duda
License: GPL-3.0 License
"""

import zlib


class ZLIBHandler:
    def compress_data(self, input_data: bytes) -> bytes:
        return zlib.compress(input_data)

    def decompress_data(self, compressed_data: bytes) -> bytes:
        return zlib.decompress(compressed_data)
