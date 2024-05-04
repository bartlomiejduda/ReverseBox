"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""
import ctypes
from ctypes import byref, c_char
from pathlib import Path


class RefpackHandler:
    def compress_data(self, input_data: bytes) -> bytes:
        return input_data  # TODO - fix this

    def decompress_data(self, compressed_data: bytes) -> bytes:
        if compressed_data[:2] != b"\x10\xFB":
            raise Exception("Wrong refpack compression header!")
        temp_buffer = (c_char * len(compressed_data) * 100)()
        try:
            refpack_dll_path: str = str(
                Path(__file__)
                .parents[1]
                .resolve()
                .joinpath("libs")
                .joinpath("refpack.dll")
            )
            refpack_dll_file = ctypes.CDLL(refpack_dll_path)
            uncompressed_data_size = refpack_dll_file.unrefpack(
                compressed_data, byref(temp_buffer), 1
            )
        except Exception as error:
            raise Exception(f"Error while decompressing refpack data! Error: {error}")
        return bytes(bytearray(temp_buffer)[:uncompressed_data_size])
