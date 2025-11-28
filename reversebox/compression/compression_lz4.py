"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import lz4.block
import lz4.frame

# LZ4 Compression

# Frame -> with signature 04 22 4D 18
# Block -> no signature


class LZ4Handler:
    def compress_data(self, input_data: bytes) -> bytes:
        return lz4.frame.compress(input_data)

    def decompress_data(self, compressed_data: bytes) -> bytes:
        return lz4.frame.decompress(compressed_data)

    def compress_raw_block_data(self, input_data: bytes) -> bytes:
        return lz4.block.compress(input_data)

    def decompress_raw_block_data(self, compressed_data: bytes) -> bytes:
        output_buffer_size: int = len(compressed_data) * 20
        return lz4.block.decompress(
            compressed_data, uncompressed_size=output_buffer_size
        )
