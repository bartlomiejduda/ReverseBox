"""
Copyright © 2022  Bartłomiej Duda
License: GPL-3.0 License
"""

from dataclasses import dataclass

from reversebox.image.image_formats import ImageFormats


@dataclass
class CRCTestEntry:
    test_data: bytes
    expected_int: int
    expected_str: str


@dataclass
class XORTestEntry:
    test_data: bytes
    key: bytes
    expected_result: bytes


@dataclass
class XORGuesserEntry:
    encrypted_data: bytes
    decrypted_data: bytes
    max_key_length: int
    expected_xor_key: bytes


@dataclass
class ROT13TestEntry:
    test_data: bytes
    key: bytes
    expected_result: bytes


@dataclass
class XORRetro64ECOTestEntry:
    test_data: bytes
    key: int
    expected_result: bytes


@dataclass
class HashTestEntry:
    test_data: bytes
    expected_result: bytes


@dataclass
class TextHashTestEntry:
    test_string: str
    expected_int: int
    expected_str: str


@dataclass
class BytesHashTestEntry:
    test_bytes: bytes
    expected_int: int
    expected_str: str


@dataclass
class PaddingTestEntry:
    test_offset: int
    test_div: int
    expected_padding: int


@dataclass
class FileExtensionTestEntry:
    file_name: str
    expected_file_extension: str


@dataclass
class GetBitsTestEntry:
    value_to_test: int
    number_of_bits: int
    position: int
    expected_result: int


@dataclass
class GetBitsStringTestEntry:
    value_to_test: int
    bits_to_fill: int
    expected_string: str


@dataclass
class ImageDecodeEncodeTestEntry:
    img_file_path: str
    debug_flag: bool
    img_width: int
    img_height: int
    bpp: int
    img_format: ImageFormats
