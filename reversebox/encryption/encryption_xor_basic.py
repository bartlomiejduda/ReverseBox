import struct


def xor_cipher_basic(input_data: bytes, key: bytes) -> bytes:
    if len(input_data) == 0:
        return b''
    if len(key) == 0:
        return input_data

    result: bytes = b''
    key_count: int = 0
    for input_byte in input_data:
        if key_count >= len(key):
            key_count = 0

        key_char = key[key_count]
        key_count += 1
        xor_result = struct.pack("B", key_char ^ input_byte)
        result += xor_result

    return result
