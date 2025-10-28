"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

# RX3 Hash - it's modified version of DJB2 Hash
# used in RX3 image files from FIFA 15 (PS Vita)


class RX3HashHandler:
    def __init__(self):
        pass

    @staticmethod
    def calculate_rx3_hash_from_string(input_string: str, hash_size: int = 8) -> int:
        h = 5321
        if hash_size == 8:
            m = 0xFFFFFFFFFFFFFFFF
        elif hash_size == 4:
            m = 0xFFFFFFFF
        else:
            raise Exception("Not supported hash size!")
        for c in input_string:
            h = (((h * 33) & m) + ord(c)) & m
        return h & m

    @staticmethod
    def calculate_rx3_hash_from_bytes(input_bytes: bytes, hash_size: int = 8) -> int:
        h = 5321
        if hash_size == 8:
            m = 0xFFFFFFFFFFFFFFFF
        elif hash_size == 4:
            m = 0xFFFFFFFF
        else:
            raise Exception("Not supported hash size!")
        for b in input_bytes:
            h = (((h * 33) & m) + b) & m
        return h & m
