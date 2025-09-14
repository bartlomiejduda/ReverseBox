"""
Copyright © 2024-2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import ctypes
import faulthandler
from ctypes import c_char

from reversebox.common.common import get_dll_path

# fmt: off


class RefpackHandler:
    """
    Compressor/Decompressor for EA Refpack algorithm
    """

    def __init__(self):
        faulthandler.enable()

    def compress_data(self, uncompressed_data: bytes) -> bytes:
        if len(uncompressed_data) == 0:
            raise Exception("Data is empty! Nothing to compress!")

        maxback: int = 131072
        quick: int = 0

        c_uncompressed_data_len = ctypes.c_uint(len(uncompressed_data))
        c_uncompressed_data = (ctypes.c_ubyte * len(uncompressed_data))(*uncompressed_data)
        c_compressed_data_buffer = (c_char * int(len(uncompressed_data)*5))()  # just in case
        c_options_maxback = ctypes.c_uint(maxback)
        c_options_quick = ctypes.c_uint(quick)

        try:
            refpack_dll_path: str = get_dll_path("refpack.dll")
            refpack_dll_file = ctypes.CDLL(refpack_dll_path)
            compressed_data_size = refpack_dll_file.refpack_compress(ctypes.byref(c_compressed_data_buffer), c_uncompressed_data, c_uncompressed_data_len, ctypes.byref(c_options_maxback), ctypes.byref(c_options_quick))
        except Exception as error:
            raise Exception(f"Error while decompressing refpack data! Error: {error}")
        return bytes(bytearray(c_compressed_data_buffer)[:compressed_data_size])

    def _get_output_buffer_size(self, compressed_data: bytes) -> int:
        current_input_offset: int = 0
        compression_type = compressed_data[current_input_offset]
        current_input_offset += 1
        compression_type = (compression_type << 8) + compressed_data[current_input_offset]
        current_input_offset += 1

        if compression_type & 0x100:
            current_input_offset += 3  # skip uncompressed_size

        uncompressed_size: int = compressed_data[current_input_offset]
        current_input_offset += 1
        uncompressed_size = (uncompressed_size << 8) + compressed_data[current_input_offset]
        current_input_offset += 1
        uncompressed_size = (uncompressed_size << 8) + compressed_data[current_input_offset]
        current_input_offset += 1
        return uncompressed_size

    def decompress_data(self, compressed_data: bytes) -> bytes:
        if len(compressed_data) < 5:
            raise Exception("Compressed data too short!")
        if compressed_data[:2] != b"\x10\xFB":
            raise Exception("Wrong refpack compression header!")

        uncompressed_data_buffer = (c_char * self._get_output_buffer_size(compressed_data))()
        compressed_data_len = ctypes.c_uint(len(compressed_data))

        try:
            refpack_dll_path: str = get_dll_path("refpack.dll")
            refpack_dll_file = ctypes.CDLL(refpack_dll_path)
            uncompressed_data_size = refpack_dll_file.refpack_decompress(ctypes.byref(uncompressed_data_buffer), compressed_data, ctypes.byref(compressed_data_len))
        except Exception as error:
            raise Exception(f"Error while decompressing refpack data! Error: {error}")
        return bytes(bytearray(uncompressed_data_buffer)[:uncompressed_data_size])
