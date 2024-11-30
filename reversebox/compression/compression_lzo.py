"""
Copyright © 2022  Bartłomiej Duda
License: GPL-3.0 License
"""

import lzokay


class LZOHandler:
    def compress_data(self, input_data: bytes) -> bytes:
        return lzokay.compress(input_data)

    def decompress_data(self, compressed_data: bytes) -> bytes:
        return lzokay.decompress(compressed_data)
