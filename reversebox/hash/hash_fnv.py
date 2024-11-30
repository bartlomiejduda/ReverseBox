"""
Copyright © 2023  Bartłomiej Duda
License: GPL-3.0 License
"""

import struct
import sys

FNV_32_PRIME: int = 0x01000193
FNV_64_PRIME: int = 0x100000001B3

FNV0_32_INIT: int = 0
FNV0_64_INIT: int = 0
FNV1_32_INIT: int = 0x811C9DC5
FNV1_32A_INIT: int = FNV1_32_INIT
FNV1_64_INIT: int = 0xCBF29CE484222325
FNV1_64A_INIT: int = FNV1_64_INIT


if sys.version_info[0] == 3:
    _get_byte = lambda c: c  # noqa: E731
else:
    _get_byte = ord


class FNVHashHandler:
    def __init__(self):
        pass

    def fnv1(self, data: bytes, hval_init, fnv_prime, fnv_size) -> int:
        hash_value: int = hval_init
        for byte in data:
            hash_value = (hash_value * fnv_prime) % fnv_size
            hash_value = hash_value ^ _get_byte(byte)
        return hash_value

    def fnva(self, data: bytes, hval_init, fnv_prime, fnv_size) -> int:
        hash_value: int = hval_init
        for byte in data:
            hash_value = hash_value ^ _get_byte(byte)
            hash_value = (hash_value * fnv_prime) % fnv_size
        return hash_value

    def fnv0_32(self, data: bytes, hval_init=FNV0_32_INIT) -> bytes:
        return struct.pack("<I", self.fnv1(data, hval_init, FNV_32_PRIME, 2**32))

    def fnv1_32(self, data: bytes, hval_init=FNV1_32_INIT) -> bytes:
        return struct.pack("<I", self.fnv1(data, hval_init, FNV_32_PRIME, 2**32))

    # used in "Mercenaries: Playground of Destruction" xbox game
    # used by "WinHash" program
    def fnv1a_32(self, data: bytes, hval_init=FNV1_32_INIT) -> bytes:
        return struct.pack("<I", self.fnva(data, hval_init, FNV_32_PRIME, 2**32))

    def fnv0_64(self, data: bytes, hval_init=FNV0_64_INIT) -> bytes:
        return struct.pack("<I", self.fnv1(data, hval_init, FNV_64_PRIME, 2**64))

    def fnv1_64(self, data: bytes, hval_init=FNV1_64_INIT) -> bytes:
        return struct.pack("<I", self.fnv1(data, hval_init, FNV_64_PRIME, 2**64))

    def fnv1a_64(self, data: bytes, hval_init=FNV1_64_INIT) -> bytes:
        return struct.pack("<I", self.fnva(data, hval_init, FNV_64_PRIME, 2**64))
