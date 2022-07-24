"""
Copyright © 2022  Bartłomiej Duda
License: GPL-3.0 License
"""

CRC_START_MODBUS = 0xFFFF
CRC_POLY_MODBUS = 0xA001


class CRC16MODBUSHandler:
    def __init__(self):
        self.crc16_modbus_tab_calculated: bool = False
        self.crc16_modbus_tab = []

    def calculate_crc16_modbus(self, input_data: bytes) -> int:
        crc: int = CRC_START_MODBUS

        if not self.crc16_modbus_tab_calculated:
            self.init_crc16_modbus_tab()

        for byte in input_data:
            short_c = 0x00FF & byte
            tmp = crc ^ short_c
            crc = (crc >> 8) ^ self.crc16_modbus_tab[tmp & 0xFF]

        return crc & 0xFFFF

    def init_crc16_modbus_tab(self):
        for i in range(256):
            crc = 0
            c = i
            for j in range(8):
                if (crc ^ c) & 0x0001:
                    crc = (crc >> 1) ^ CRC_POLY_MODBUS
                else:
                    crc = crc >> 1

                c = c >> 1

            self.crc16_modbus_tab.append(crc)

        self.crc16_modbus_tab_calculated = True
