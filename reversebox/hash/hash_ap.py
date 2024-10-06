"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""


class APHandler:
    def __init__(self):
        pass

    @staticmethod
    def calculate_ap_hash_from_string(input_string: str) -> int:
        hash_value = 0xAAAAAAAA
        i = 0
        for char in input_string:
            if i & 1 == 0:
                hash_value ^= (hash_value << 7) ^ ord(char) * (hash_value >> 3)
            else:
                hash_value ^= ~((hash_value << 11) + ord(char) ^ (hash_value >> 5))
            i += 1
        return hash_value & 0xFFFFFFFF

    @staticmethod
    def calculate_ap_hash_from_bytes(input_bytes: bytes) -> int:
        hash_value = 0xAAAAAAAA
        i = 0
        for char in input_bytes:
            if i & 1 == 0:
                hash_value ^= (hash_value << 7) ^ char * (hash_value >> 3)
            else:
                hash_value ^= ~((hash_value << 11) + char ^ (hash_value >> 5))
            i += 1
        return hash_value & 0xFFFFFFFF
