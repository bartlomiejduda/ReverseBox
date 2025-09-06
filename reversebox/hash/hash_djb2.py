"""
Copyright © 2024-2025  Bartłomiej Duda
License: GPL-3.0 License
"""


# Bernstein's DJB2 hash
# used in EA BIG VIV EB archives to calculate hash from file paths
# used in VFS archives from "Room of Prey" Android games
class DJB2Handler:
    def __init__(self):
        pass

    @staticmethod
    def calculate_djb2_hash_from_string(input_string: str, hash_size: int = 8) -> int:
        h = 5381
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
    def calculate_djb2_hash_from_bytes(input_bytes: bytes, hash_size: int = 8) -> int:
        h = 5381
        if hash_size == 8:
            m = 0xFFFFFFFFFFFFFFFF
        elif hash_size == 4:
            m = 0xFFFFFFFF
        else:
            raise Exception("Not supported hash size!")
        for b in input_bytes:
            h = (((h * 33) & m) + b) & m
        return h & m
