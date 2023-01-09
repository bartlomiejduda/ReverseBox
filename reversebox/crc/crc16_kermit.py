"""
Copyright © 2022  Bartłomiej Duda
License: GPL-3.0 License
"""

CRC_START_KERMIT = 0x0000
CRC_POLY_KERMIT = 0x8408


class CRC16KermitHandler:
    def __init__(self):
        self.crc16_kermit_tab_calculated: bool = False
        self.crc16_kermit_tab = []

    def calculate_crc16_kermit(self, input_data: bytes) -> int:
        crc: int = CRC_START_KERMIT

        if not self.crc16_kermit_tab_calculated:
            self.init_crc16_kermit_tab()

        for byte in input_data:
            short_c = 0x00FF & byte
            tmp = crc ^ short_c
            crc = (crc >> 8) ^ self.crc16_kermit_tab[tmp & 0xFF]

        low_byte = (crc & 0xFF00) >> 8
        high_byte = (crc & 0x00FF) << 8
        crc = low_byte | high_byte
        return crc

    def init_crc16_kermit_tab(self):
        for i in range(256):
            crc = 0
            c = i
            for j in range(8):
                if (crc ^ c) & 0x0001:
                    crc = (crc >> 1) ^ CRC_POLY_KERMIT
                else:
                    crc = crc >> 1

                c = c >> 1

            self.crc16_kermit_tab.append(crc)

        self.crc16_kermit_tab_calculated = True
