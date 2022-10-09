"""
Copyright © 2022  Bartłomiej Duda
License: GPL-3.0 License
"""

import hashlib


class MD5Handler:
    def __init__(self):
        pass

    @staticmethod
    def calculate_md5_hash(input_data: bytes) -> bytes:
        return hashlib.md5(input_data).digest()
