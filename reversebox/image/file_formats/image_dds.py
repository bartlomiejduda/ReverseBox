"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""
import struct

from reversebox.common.logger import get_logger

logger = get_logger(__name__)


class DDS_Image:
    # surface header
    signature: bytes = b"DDS\x20"
    header_size: int = 124
    header_flags: int = 4103
    image_height: int = 0
    image_width: int = 0
    pitch: int = 0
    depth: int = 0
    number_of_mipmaps: int = 0
    reserved_1 = b"\x00" * 44

    # pixel format info
    info_size: int = 32
    info_flags: int = 65
    compression_type: bytes = b"\x00\x00\x00\x00"
    rgb_bit_count: int = 32
    r_bit_mask: bytes = b"\xFF\x00\x00\x00"
    g_bit_mask: bytes = b"\x00\xFF\x00\x00"
    b_bit_mask: bytes = b"\x00\x00\xFF\x00"
    a_bit_mask: bytes = b"\x00\x00\x00\xFF"

    # capabilities
    caps_1: int = 4098
    caps_2: int = 0
    caps_reserved_1: int = 0
    caps_reserved_2: int = 0

    # reserved
    reserved_2 = 0

    # image
    image_data = b""

    def __init__(self, width: int, height: int, image_data: bytes):
        self.image_width = width
        self.image_height = height
        self.image_data = image_data

    def get_file_data(self):
        def _pack_4_bytes(value) -> bytes:
            return struct.pack("<L", value)

        def _pack_header() -> bytes:
            return (
                self.signature
                + _pack_4_bytes(self.header_size)
                + _pack_4_bytes(self.header_flags)
                + _pack_4_bytes(self.image_height)
                + _pack_4_bytes(self.image_width)
                + _pack_4_bytes(self.pitch)
                + _pack_4_bytes(self.depth)
                + _pack_4_bytes(self.number_of_mipmaps)
                + self.reserved_1
            )

        def _pack_pixel_format_info() -> bytes:
            return (
                _pack_4_bytes(self.info_size)
                + _pack_4_bytes(self.info_flags)
                + self.compression_type
                + _pack_4_bytes(self.rgb_bit_count)
                + self.r_bit_mask
                + self.g_bit_mask
                + self.b_bit_mask
                + self.a_bit_mask
            )

        def _pack_capabilities() -> bytes:
            return (
                _pack_4_bytes(self.caps_1)
                + _pack_4_bytes(self.caps_2)
                + _pack_4_bytes(self.caps_reserved_1)
                + _pack_4_bytes(self.caps_reserved_2)
            )

        def _pack_reserved() -> bytes:
            return _pack_4_bytes(self.reserved_2)

        file_data: bytes = (
            _pack_header()
            + _pack_pixel_format_info()
            + _pack_capabilities()
            + _pack_reserved()
            + self.image_data
        )

        return file_data
