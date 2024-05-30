"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""


class Sum82sComplementHandler:
    def __init__(self):
        pass

    def calculate_sum8_2s_complement(self, input_data: bytes) -> int:
        s = 0
        for input_byte in input_data:
            s += input_byte & 0xFF
        checksum = (0x100 - s) & 0xFF
        return checksum