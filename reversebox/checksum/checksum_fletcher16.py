"""
Copyright © 2023  Bartłomiej Duda
License: GPL-3.0 License
"""


class Fletcher16Handler:
    def __init__(self):
        pass

    def calculate_fletcher16(self, input_data: bytes) -> int:
        sum1 = 0
        sum2 = 0
        for input_byte in input_data:
            sum1 = (sum1 + input_byte) % 255
            sum2 = (sum2 + sum1) % 255
        return (sum2 << 8) | sum1
