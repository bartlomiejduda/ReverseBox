import struct

import rawutil


def get_bits(number: int, number_of_bits: int, position: int) -> int:
    return ((1 << number_of_bits) - 1) & (number >> position)


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
