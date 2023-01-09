"""
Copyright © 2022  Bartłomiej Duda
License: GPL-3.0 License
"""

CRC_START_SICK = 0x0000
CRC_POLY_SICK = 0x8005


class CRC16SICKHandler:
    def __init__(self):
        pass

    def calculate_crc16_sick(self, input_data: bytes) -> int:
        crc: int = CRC_START_SICK
        short_p = 0

        for byte in input_data:
            short_c = 0x00FF & byte

            if crc & 0x8000:
                crc = (crc << 1) ^ CRC_POLY_SICK
            else:
                crc = crc << 1

            crc ^= short_c | short_p
            short_p = short_c << 8

        low_byte = (crc & 0xFF00) >> 8
        high_byte = (crc & 0x00FF) << 8
        crc = low_byte | high_byte

        return crc
