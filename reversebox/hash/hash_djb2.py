"""
Copyright © 2024-2025  Bartłomiej Duda
License: GPL-3.0 License
"""


# Bernstein's DJB2 hash
# used in EA BIG VIV EB archives to calculate hash from file paths
class DJB2Handler:
    def __init__(self):
        pass

    @staticmethod
    def calculate_djb2_hash_from_string(input_string: str) -> int:
        h = 5381
        m = 0xFFFFFFFFFFFFFFFF
        for c in input_string:
            h = (((h * 33) & m) + ord(c)) & m
        return h & m

    @staticmethod
    def calculate_djb2_hash_from_bytes(input_bytes: bytes) -> int:
        h = 5381
        m = 0xFFFFFFFFFFFFFFFF
        for b in input_bytes:
            h = (((h * 33) & m) + b) & m
        return h & m
