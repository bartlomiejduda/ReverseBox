"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""
import ctypes
from ctypes import byref, c_char

from reversebox.common.common import get_dll_path


class RefpackHandler:
    def compress_data(self, input_data: bytes) -> bytes:
        return input_data  # TODO - fix this

    def _get_output_buffer_size(self, compressed_data: bytes) -> int:
        current_input_offset: int = 0
        compression_type = compressed_data[current_input_offset]
        current_input_offset += 1
        compression_type = (compression_type << 8) + compressed_data[
            current_input_offset
        ]
        current_input_offset += 1

        if compression_type & 0x100:
            current_input_offset += 3  # skip uncompressed_size

        uncompressed_size: int = compressed_data[current_input_offset]
        current_input_offset += 1
        uncompressed_size = (uncompressed_size << 8) + compressed_data[
            current_input_offset
        ]
        current_input_offset += 1
        uncompressed_size = (uncompressed_size << 8) + compressed_data[
            current_input_offset
        ]
        current_input_offset += 1
        return uncompressed_size

    def decompress_data(self, compressed_data: bytes) -> bytes:
        if len(compressed_data) < 5:
            raise Exception("Compressed data too short!")
        if compressed_data[:2] != b"\x10\xFB":
            raise Exception("Wrong refpack compression header!")
        uncompressed_data_buffer = (
            c_char * self._get_output_buffer_size(compressed_data)
        )()
        try:
            refpack_dll_path: str = get_dll_path("refpack.dll")
            refpack_dll_file = ctypes.CDLL(refpack_dll_path)
            uncompressed_data_size = refpack_dll_file.unrefpack(
                compressed_data, byref(uncompressed_data_buffer), 1
            )
        except Exception as error:
            raise Exception(f"Error while decompressing refpack data! Error: {error}")
        return bytes(bytearray(uncompressed_data_buffer)[:uncompressed_data_size])
