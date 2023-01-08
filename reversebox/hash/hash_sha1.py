"""
Copyright © 2023  Bartłomiej Duda
License: GPL-3.0 License
"""

import hashlib


class SHA1Handler:
    def __init__(self):
        pass

    @staticmethod
    def calculate_sha1_hash(input_data: bytes) -> bytes:
        return hashlib.sha1(input_data).digest()
