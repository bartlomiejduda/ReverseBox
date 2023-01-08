"""
Copyright © 2023  Bartłomiej Duda
License: GPL-3.0 License
"""

MOD_ADLER = 65521


class Adler32Handler:
    def __init__(self):
        pass

    def calculate_adler32(self, input_data: bytes) -> int:
        a = 1
        b = 0
        for input_byte in input_data:
            a = (a + input_byte) % MOD_ADLER
            b = (b + a) % MOD_ADLER
        return (b << 16) | a
