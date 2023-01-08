"""
Copyright © 2023  Bartłomiej Duda
License: GPL-3.0 License
"""

import hashlib


class SHA2Handler:
    def __init__(self):
        pass

    @staticmethod
    def calculate_sha2_256_hash(input_data: bytes) -> bytes:
        return hashlib.sha256(input_data).digest()
