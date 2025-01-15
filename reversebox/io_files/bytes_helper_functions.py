"""
Copyright © 2024-2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import struct


# e.g. number=2273, number_of_bits=3, position=5  result --> 7
def get_bits(number: int, number_of_bits: int, position: int) -> int:
    return ((1 << number_of_bits) - 1) & (number >> position)


# e.g. number=171, bits_to_fill=16  result --> 0000000010101011
def get_bits_string(number: int, bits_to_fill: int) -> str:
    return bin(number).lstrip("0b").zfill(bits_to_fill)


def _get_int_from_bytes_value(
    signed_flag: bool, input_bytes: bytes, endianess: str
) -> int:
    if endianess == "<":
        return int.from_bytes(input_bytes, signed=signed_flag, byteorder="little")
    elif endianess == ">":
        return int.from_bytes(input_bytes, signed=signed_flag, byteorder="big")
    else:
        raise Exception("Endianess not supported!")


def _set_int_to_bytes_value(
    signed_flag: bool, bytes_length: int, input_value: int, endianess: str
) -> bytes:
    if endianess == "<":
        return input_value.to_bytes(bytes_length, "little", signed=signed_flag)
    elif endianess == ">":
        return input_value.to_bytes(bytes_length, "big", signed=signed_flag)
    else:
        raise Exception("Endianess not supported!")


def _check_input_bytes_size(input_bytes: bytes, expected_size: int) -> None:
    if len(input_bytes) != expected_size:
        raise ValueError(f"Input must be exactly {expected_size} bytes long.")


def get_int8(input_bytes: bytes, endianess: str) -> int:
    _check_input_bytes_size(input_bytes, 1)
    return struct.unpack(endianess + "b", input_bytes)[0]


def get_uint8(input_bytes: bytes, endianess: str) -> int:
    _check_input_bytes_size(input_bytes, 1)
    return struct.unpack(endianess + "B", input_bytes)[0]


def get_int16(input_bytes: bytes, endianess: str) -> int:
    _check_input_bytes_size(input_bytes, 2)
    return struct.unpack(endianess + "h", input_bytes)[0]


def get_uint16(input_bytes: bytes, endianess: str) -> int:
    _check_input_bytes_size(input_bytes, 2)
    return struct.unpack(endianess + "H", input_bytes)[0]


def get_int24(input_bytes: bytes, endianess: str) -> int:
    _check_input_bytes_size(input_bytes, 3)
    return _get_int_from_bytes_value(True, input_bytes, endianess)


def get_uint24(input_bytes: bytes, endianess: str) -> int:
    _check_input_bytes_size(input_bytes, 3)
    return _get_int_from_bytes_value(False, input_bytes, endianess)


def get_int32(input_bytes: bytes, endianess: str) -> int:
    _check_input_bytes_size(input_bytes, 4)
    return struct.unpack(endianess + "i", input_bytes)[0]


def get_uint32(input_bytes: bytes, endianess: str) -> int:
    _check_input_bytes_size(input_bytes, 4)
    return struct.unpack(endianess + "I", input_bytes)[0]


def get_int48(input_bytes: bytes, endianess: str) -> int:
    _check_input_bytes_size(input_bytes, 6)
    return _get_int_from_bytes_value(True, input_bytes, endianess)


def get_uint48(input_bytes: bytes, endianess: str) -> int:
    _check_input_bytes_size(input_bytes, 6)
    return _get_int_from_bytes_value(False, input_bytes, endianess)


def get_int64(input_bytes: bytes, endianess: str) -> int:
    _check_input_bytes_size(input_bytes, 8)
    return struct.unpack(endianess + "q", input_bytes)[0]


def get_uint64(input_bytes: bytes, endianess: str) -> int:
    _check_input_bytes_size(input_bytes, 8)
    return struct.unpack(endianess + "Q", input_bytes)[0]


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
    return _set_int_to_bytes_value(True, 3, input_value, endianess)


def set_uint24(input_value: int, endianess: str) -> bytes:
    return _set_int_to_bytes_value(False, 3, input_value, endianess)


def set_int32(input_value: int, endianess: str) -> bytes:
    return struct.pack(endianess + "i", input_value)


def set_uint32(input_value: int, endianess: str) -> bytes:
    return struct.pack(endianess + "I", input_value)


def set_int48(input_value: int, endianess: str) -> bytes:
    return _set_int_to_bytes_value(True, 6, input_value, endianess)


def set_uint48(input_value: int, endianess: str) -> bytes:
    return _set_int_to_bytes_value(False, 6, input_value, endianess)


def set_int64(input_value: int, endianess: str) -> bytes:
    return struct.pack(endianess + "q", input_value)


def set_uint64(input_value: int, endianess: str) -> bytes:
    return struct.pack(endianess + "Q", input_value)
