"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""
import ctypes
from ctypes import c_char
from pathlib import Path


class RefpackHandler:
    def compress_data(self, input_data: bytes) -> bytes:
        return input_data  # TODO - fix this

    def decompress_data(self, compressed_data: bytes) -> bytes:
        temp_buffer = (c_char * len(compressed_data) * 10)()
        refpack_dll_path: str = str(
            Path(__file__).parents[1].resolve().joinpath("libs").joinpath("refpack.dll")
        )
        refpack_dll_file = ctypes.cdll.LoadLibrary(refpack_dll_path)
        uncompressed_data_size = refpack_dll_file.unrefpack(
            compressed_data, temp_buffer
        )
        return bytes(bytearray(temp_buffer)[:uncompressed_data_size])
