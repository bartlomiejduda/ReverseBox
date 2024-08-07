"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

import struct

import rawutil


# e.g. number=2273, number_of_bits=3, position=5  result --> 7
def get_bits(number: int, number_of_bits: int, position: int) -> int:
    return ((1 << number_of_bits) - 1) & (number >> position)


# e.g. number=171, bits_to_fill=16  result --> 0000000010101011
def get_bits_string(number: int, bits_to_fill: int) -> str:
    return bin(number).lstrip("0b").zfill(bits_to_fill)


def get_int8(input_bytes: bytes, endianess: str) -> int:
    return struct.unpack(endianess + "b", input_bytes)[0]


def get_uint8(input_bytes: bytes, endianess: str) -> int:
    return struct.unpack(endianess + "B", input_bytes)[0]


def get_int16(input_bytes: bytes, endianess: str) -> int:
    return struct.unpack(endianess + "h", input_bytes)[0]


def get_uint16(input_bytes: bytes, endianess: str) -> int:
    return struct.unpack(endianess + "H", input_bytes)[0]


def get_int24(input_bytes: bytes, endianess: str) -> int:
    return rawutil.unpack(endianess + "u", input_bytes)[0]


def get_uint24(input_bytes: bytes, endianess: str) -> int:
    return rawutil.unpack(endianess + "U", input_bytes)[0]


def get_int32(input_bytes: bytes, endianess: str) -> int:
    return struct.unpack(endianess + "i", input_bytes)[0]


def get_uint32(input_bytes: bytes, endianess: str) -> int:
    return struct.unpack(endianess + "I", input_bytes)[0]


#####
#####
#####


def set_int8(input_value: int, endianess: str) -> bytes:
    return struct.pack(endianess + "b", input_value)


def set_uint8(input_value: int, endianess: str) -> bytes:
    return struct.pack(endianess + "B", input_value)


def set_int16(input_value: int, endianess: str) -> bytes:
    return struct.pack(endianess + "h", input_value)


def set_uint16(input_value: int, endianess: str) -> bytes:
    return struct.pack(endianess + "H", input_value)


def set_int24(input_value: int, endianess: str) -> bytes:
    return rawutil.pack(endianess + "u", input_value)


def set_uint24(input_value: int, endianess: str) -> bytes:
    return rawutil.pack(endianess + "U", input_value)


def set_int32(input_value: int, endianess: str) -> bytes:
    return struct.pack(endianess + "i", input_value)


def set_uint32(input_value: int, endianess: str) -> bytes:
    return struct.pack(endianess + "I", input_value)
