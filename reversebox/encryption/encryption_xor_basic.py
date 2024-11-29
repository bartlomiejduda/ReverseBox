"""
Copyright © 2022-2024  Bartłomiej Duda
License: GPL-3.0 License
"""


def xor_cipher_basic(input_data: bytes, key: bytes) -> bytes:
    if len(input_data) == 0:
        return b""
    if len(key) == 0:
        return input_data

    result: bytearray = bytearray(len(input_data))
    key_count: int = 0
    data_count: int = 0
    for input_byte in input_data:
        if key_count >= len(key):
            key_count = 0

        key_char = key[key_count]
        key_count += 1
        result[data_count] = key_char ^ input_byte
        data_count += 1

    return result
