"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

from crc import Calculator, Configuration


class CRC64GoISOHandler:
    def __init__(self):
        pass

    def calculate_crc64(self, input_data: bytes) -> int:
        config = Configuration(
            width=64,
            polynomial=0x000000000000001B,
            init_value=0xFFFFFFFFFFFFFFFF,
            final_xor_value=0xFFFFFFFFFFFFFFFF,
            reverse_input=True,
            reverse_output=True,
        )
        calculator = Calculator(config)
        return calculator.checksum(input_data)
