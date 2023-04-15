"""
Copyright © 2023  Bartłomiej Duda
License: GPL-3.0 License
"""

import struct
from itertools import cycle

# XOR Cipher used in Giana's Return *.ZDA files
# Read more here: http://wiki.xentax.com/index.php/Giana%E2%80%99s_Return_ZDA

# Thanks to Zigaudrey for help with writing encrypt function


def xor_zda_decrypt_data(input_data: bytes) -> bytes:
    xor_res = b"\xBB"
    data_size = len(input_data)
    out_data = bytearray()

    for curr_offset in range(data_size):
        data_byte = struct.pack("B", input_data[curr_offset])
        xor_res = bytes(a ^ b for a, b in zip(xor_res, cycle(data_byte)))
        out_data.extend(xor_res)
    return out_data


def xor_zda_encrypt_data(input_data: bytes) -> bytes:
    data_size = len(input_data)
    out_data = bytearray()
    key_data: bytes = b"\xBB" + input_data

    for curr_offset in range(data_size):
        xor_res = bytes(
            a ^ b
            for a, b in zip(
                struct.pack("B", input_data[curr_offset]),
                struct.pack("B", key_data[curr_offset]),
            )
        )
        out_data.extend(xor_res)
    return out_data
