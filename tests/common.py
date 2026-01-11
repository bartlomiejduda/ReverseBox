"""
Copyright © 2022-2024  Bartłomiej Duda
License: GPL-3.0 License
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional

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
    seed: Optional[int] = None
    prime: Optional[int] = None
    hash_size: Optional[int] = None


@dataclass
class BytesHashTestEntry:
    test_bytes: bytes
    expected_int: int
    expected_str: str
    seed: Optional[int] = None
    prime: Optional[int] = None
    hash_size: Optional[int] = None


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
class GetSetBytesEntry:
    value_int: int
    value_bytes: bytes
    endianess: str


class EncodeIndexedMethod(str, Enum):
    V1 = "V1"
    V2 = "V2"


@dataclass
class ImageDecodeEncodeTestEntry:
    img_file_path: str
    debug_flag: bool
    img_width: int
    img_height: int
    img_format: ImageFormats
    pal_file_path: Optional[str] = None
    pal_format: Optional[ImageFormats] = None
    bpp: Optional[int] = None
    palette_offset: Optional[int] = None
    palette_size: Optional[int] = None
    image_data_offset: Optional[int] = None
    image_data_size: Optional[int] = None
    max_colors_count: Optional[int] = None
    number_of_mipmaps: Optional[int] = None
    image_endianess: Optional[str] = None
    encode_indexed_method: Optional[EncodeIndexedMethod] = None


@dataclass
class ImagePerformanceTestEntry:
    test_id: int
    img_format: ImageFormats
    execution_time: float


@dataclass
class GSTSwizzleTestEntry:
    img_path: str
    pal_path: str
    debug_flag: bool
    img_width: int
    img_height: int
    img_format: ImageFormats
    conv_format: ImageFormats
    conv_pal_format: ImageFormats


@dataclass
class MortonIndexTestEntry:
    t: int
    width: int
    height: int
    expected_result: int
