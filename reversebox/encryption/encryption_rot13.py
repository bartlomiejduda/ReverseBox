"""
Copyright © 2023  Bartłomiej Duda
License: GPL-3.0 License
"""

import struct


def rot13_cipher_encrypt(input_data: bytes, key: bytes) -> bytes:
    if len(input_data) == 0:
        return b""
    if len(key) == 0:
        return input_data

    result: bytes = b""
    key_count: int = 0
    for input_byte in input_data:
        if key_count >= len(key):
            key_count = 0

        key_char = key[key_count]
        key_count += 1
        rot_result = struct.pack("B", (key_char + input_byte) & 0xFF)
        result += rot_result

    return result


def rot13_cipher_decrypt(input_data: bytes, key: bytes) -> bytes:
    if len(input_data) == 0:
        return b""
    if len(key) == 0:
        return input_data

    result: bytes = b""
    key_count: int = 0
    for input_byte in input_data:
        if key_count >= len(key):
            key_count = 0

        key_char = key[key_count]
        key_count += 1
        rot_result = struct.pack("B", (input_byte - key_char) & 0xFF)
        result += rot_result

    return result
