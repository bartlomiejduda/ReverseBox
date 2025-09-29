"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import struct

# Custom Huffman compression used in games made by "Intelligent Games"
# https://rewiki.miraheze.org/wiki/Intelligent_Games_RFH_RFD


def huffman_decompress_data(data: bytes) -> bytes:
    decompressed_size: int = struct.unpack_from("<L", data, 0)[0]
    root: int = struct.unpack_from("<H", data, 4)[0]
    node: int = root
    output: bytearray = bytearray()

    for byte_position in range(0x808, len(data)):
        bits = data[byte_position]

        for _ in range(8):
            bit = bits & 1
            bits >>= 1
            node_position = (node * 4) + (bit * 2) + 8
            node = struct.unpack_from("<H", data, node_position)[0]

            is_terminal: bool = (node & 0x100) == 0
            if is_terminal:
                output.append(node & 0xFF)
                node = root
                if len(output) >= decompressed_size:
                    break

            if len(output) >= decompressed_size:
                break

    return bytes(output)
