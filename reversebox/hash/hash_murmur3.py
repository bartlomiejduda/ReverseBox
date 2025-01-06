"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import mmh3


class Murmur3Handler:
    def __init__(self):
        pass

    @staticmethod
    def calculate_murmur3_hash_from_string(key: str, seed: int = 0xDEADBEEF) -> int:
        return mmh3.hash(key=key, seed=seed, signed=False)

    @staticmethod
    def calculate_murmur3_hash_from_bytes(key: bytes, seed: int = 0xDEADBEEF) -> int:
        return mmh3.hash(key=key, seed=seed, signed=False)
