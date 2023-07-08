"""
Copyright © 2023  Bartłomiej Duda
License: GPL-3.0 License
"""

from crc import Calculator, Configuration

CRC_START_8 = 0x00
CRC_POLY_8 = 0x07

CRC_START_8_CDMA_2000 = 0xFF
CRC_POLY_8_CDMA_2000 = 0x9B


class CRC8Handler:
    def __init__(self):
        pass

    def calculate_crc8(self, input_data: bytes) -> int:
        return self.calculate_crc8_base(input_data, CRC_START_8, CRC_POLY_8)

    def calculate_crc8_cdma_2000(self, input_data: bytes) -> int:
        return self.calculate_crc8_base(
            input_data, CRC_START_8_CDMA_2000, CRC_POLY_8_CDMA_2000
        )

    def calculate_crc8_darc(self, input_data: bytes) -> int:
        config = Configuration(
            width=8,
            polynomial=0x39,
            init_value=0x00,
            final_xor_value=0x00,
            reverse_input=True,
            reverse_output=True,
        )
        calculator = Calculator(config)
        return calculator.checksum(input_data)

    def calculate_crc8_base(
        self, input_data: bytes, crc_start: int, crc_poly: int
    ) -> int:
        crc = crc_start
        for byte in input_data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x80:
                    crc = (crc << 1) ^ crc_poly
                else:
                    crc <<= 1
                crc &= 0xFF
        return crc
