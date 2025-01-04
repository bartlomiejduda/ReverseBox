"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

from reversebox.crc.crc32_iso_hdlc import CRC32Handler
from reversebox.io_files.bytes_helper_functions import set_uint32, set_uint64

# Encryption algorithm used in Hatch Engine games
# e.g. Data.hatch archive from "Sonic Galactic" (Demo 2) game


def decrypt_hatch_data(f_data: bytes, filename: str, f_size: int) -> bytes:
    crc_handler = CRC32Handler()
    keyA: bytearray = bytearray(16)
    keyB: bytearray = bytearray(16)
    decrypted_data: bytearray = bytearray(f_data)

    filename_hash: int = crc_handler.calculate_crc32(filename.encode("ascii"))
    encoded_filename_hash: bytes = set_uint32(filename_hash, "<")
    encoded_size_value: bytes = set_uint64(f_size, "<")
    size_hash: int = crc_handler.calculate_crc32(encoded_size_value)
    encoded_size_hash: bytes = set_uint32(size_hash, "<")

    for i in range(4):
        keyA[i * 4 : (i + 1) * 4] = encoded_filename_hash

    for i in range(4):
        keyB[i * 4 : (i + 1) * 4] = encoded_size_hash

    swap_nibbles: int = 0
    index_keyA: int = 0
    index_keyB: int = 8

    xor_value = (f_size >> 2) & 0x7F

    for x in range(f_size):
        temp = decrypted_data[x]

        temp ^= xor_value ^ keyB[index_keyB]
        index_keyB += 1

        if swap_nibbles:
            temp = ((temp & 0x0F) << 4) | ((temp & 0xF0) >> 4)

        temp ^= keyA[index_keyA]
        index_keyA += 1

        decrypted_data[x] = temp

        if index_keyA <= 15:
            if index_keyB > 12:
                index_keyB = 0
                swap_nibbles ^= 1
        elif index_keyB <= 8:
            index_keyA = 0
            swap_nibbles ^= 1
        else:
            xor_value = (xor_value + 2) & 0x7F
            if swap_nibbles:
                swap_nibbles = 0
                index_keyA = xor_value % 7
                index_keyB = (xor_value % 12) + 2
            else:
                swap_nibbles = 1
                index_keyA = (xor_value % 12) + 3
                index_keyB = xor_value % 7

    return decrypted_data
