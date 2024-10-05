"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""


class SDBMHandler:
    def __init__(self):
        pass

    # used in Forza Horizon (2012)
    @staticmethod
    def calculate_sdbm_hash_from_string(input_string: str) -> int:
        hash_value = 0
        for char in input_string:
            hash_value = ord(char) + (hash_value << 6) + (hash_value << 16) - hash_value
        return hash_value & 0xFFFFFFFF

    @staticmethod
    def calculate_sdbm_hash_from_bytes(input_bytes: bytes) -> int:
        hash_value = 0
        for char in input_bytes:
            hash_value = char + (hash_value << 6) + (hash_value << 16) - hash_value
        return hash_value & 0xFFFFFFFF
