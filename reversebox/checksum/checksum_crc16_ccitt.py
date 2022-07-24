"""
Copyright © 2022  Bartłomiej Duda
License: GPL-3.0 License
"""

CRC_POLY_CCITT = 0x1021

CRC_START_CCITT_FFFF = 0xFFFF
CRC_START_CCITT_1D0F = 0x1D0F
CRC_START_CCITT_XMODEM = 0x0000


class CRC16CCITTHandler:
    def __init__(self):
        self.crc16_ccitt_calculated: bool = False
        self.crc16_ccitt_tab = []
        pass

    def calculate_crc16_ccitt_ffff(self, input_data: bytes) -> int:
        return self.calculate_crc16_ccitt_basic(input_data, CRC_START_CCITT_FFFF)

    def calculate_crc16_ccitt_1d0f(self, input_data: bytes) -> int:
        return self.calculate_crc16_ccitt_basic(input_data, CRC_START_CCITT_1D0F)

    def calculate_crc16_ccitt_xmodem(self, input_data: bytes) -> int:
        return self.calculate_crc16_ccitt_basic(input_data, CRC_START_CCITT_XMODEM)

    def calculate_crc16_ccitt_basic(self, input_data: bytes, crc_start: int) -> int:
        crc: int = crc_start

        if not self.crc16_ccitt_calculated:
            self.init_crc16_ccitt_tab()

        for byte in input_data:
            short_c = 0x00FF & byte
            tmp = (crc >> 8) ^ short_c
            crc = (crc << 8) ^ self.crc16_ccitt_tab[tmp & 0xFF]

        return crc & 0xFFFF

    def init_crc16_ccitt_tab(self):
        for i in range(256):
            crc = 0
            c = i << 8
            for j in range(8):
                if (crc ^ c) & 0x8000:
                    crc = (crc << 1) ^ CRC_POLY_CCITT
                else:
                    crc = crc << 1

                c = c << 1

            self.crc16_ccitt_tab.append(crc)

        self.crc16_ccitt_calculated = True
