"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

from typing import Literal

# Mio0 compression
# used in N64 games
# https://hack64.net/wiki/doku.php?id=super_mario_64:mio0


class Mio0Handler:
    HEADER_SIZE = 0x10

    def compress_data(self, input_data: bytes) -> bytes:
        return input_data  # TODO - implement this

    def read_layout_bit(self, data, bit_idx):
        byte_index = bit_idx // 8
        bit_mod_offset = bit_idx % 8
        return data[self.HEADER_SIZE + byte_index] & (1 << (7 - bit_mod_offset))

    def decompress_data(
        self, compressed_data: bytes, endianess: Literal["little", "big"] = "big"
    ) -> bytes:
        signature: str = str(compressed_data[0x0:0x4], "ascii")

        if signature != "MIO0":
            raise ValueError('Invalid header, not starting with "MIO0"')

        decompressed_data_size = int.from_bytes(compressed_data[4:8], endianess)
        compressed_data_offset = int.from_bytes(compressed_data[8:12], endianess)
        uncompressed_data_offset = int.from_bytes(compressed_data[12:16], endianess)

        output_byte_array = bytearray()
        output_index = 0
        layout_bit_index = 0

        ci = 0
        ui = 0

        while output_index < decompressed_data_size:
            layout_bit = self.read_layout_bit(compressed_data, layout_bit_index)
            is_uncompressed = layout_bit > 0
            layout_bit_index += 1

            if output_index >= decompressed_data_size:
                break
            if is_uncompressed:
                output_byte_array.append(compressed_data[uncompressed_data_offset + ui])
                ui += 1
                output_index += 1
            else:
                len_idx_bytes = compressed_data[
                    compressed_data_offset + ci : compressed_data_offset + ci + 2
                ]
                ci += 2

                length = ((len_idx_bytes[0] & 0xF0) >> 4) + 3
                index = ((len_idx_bytes[0] & 0xF) << 8) + (len_idx_bytes[1] + 1)

                if length < 3 or length > 18:
                    raise Exception(f"wrong length value: {length}")

                if index < 1 or index > 4096:
                    raise Exception(f"wrong index value: {index}")

                for i in range(length):
                    output_byte_array.append(output_byte_array[output_index - index])
                    output_index += 1

        return bytes(output_byte_array)
