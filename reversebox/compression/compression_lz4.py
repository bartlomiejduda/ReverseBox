"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import lz4.frame


class LZ4Handler:
    def compress_data(self, input_data: bytes) -> bytes:
        return lz4.frame.compress(input_data)

    def decompress_data(self, compressed_data: bytes) -> bytes:
        return lz4.frame.decompress(compressed_data)
