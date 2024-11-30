"""
Copyright © 2023  Bartłomiej Duda
License: GPL-3.0 License
"""

from hashbase import MD2


class MD2Handler:
    def __init__(self):
        pass

    @staticmethod
    def calculate_md2_hash(input_data: bytes, encoding_type: str = "utf8") -> bytes:
        return bytes.fromhex(
            MD2().generate_hash(input_data.decode(encoding=encoding_type))
        )
