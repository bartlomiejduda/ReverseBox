"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import numpy as np


# Additive Hash
# https://www.burtleburtle.net/bob/hash/doobs.html
class AdditiveHashHandler:
    def __init__(self):
        pass

    @staticmethod
    def calculate_additive_hash_from_string(input_string: str, prime: int) -> int:
        hash_value = np.uint32(len(input_string))
        for i in range(len(input_string)):
            hash_value += np.uint8(ord(input_string[i]))
        return int(np.uint32(hash_value) % np.uint32(prime))

    @staticmethod
    def calculate_additive_hash_from_bytes(input_bytes: bytes, prime: int) -> int:
        hash_value = np.uint32(len(input_bytes))
        for i in range(len(input_bytes)):
            hash_value += np.uint8(input_bytes[i])
        return int(np.uint32(hash_value) % np.uint32(prime))
