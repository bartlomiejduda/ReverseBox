"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

import struct

import rawutil


def get_bits(number: int, number_of_bits: int, position: int) -> int:
    return ((1 << number_of_bits) - 1) & (number >> position)


# e.g. number=171, bits_to_fill=16  result --> 0000000010101011
def get_bits_string(number: int, bits_to_fill: int) -> str:
    return bin(number).lstrip("0b").zfill(bits_to_fill)


def get_uint8(input_bytes: bytes, endianess: str) -> int:
    result = struct.unpack(endianess + "B", input_bytes)[0]
    return result


def get_uint16(input_bytes: bytes, endianess: str) -> int:
    result = struct.unpack(endianess + "H", input_bytes)[0]
    return result


def get_uint24(input_bytes: bytes, endianess: str) -> int:
    result = rawutil.unpack(endianess + "U", input_bytes)[0]
    return result


def get_uint32(input_bytes: bytes, endianess: str) -> int:
    result = struct.unpack(endianess + "I", input_bytes)[0]
    return result
