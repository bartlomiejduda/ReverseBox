CRC_START_16 = 0x0000
CRC_POLY_16 = 0xA001


class CRC16Handler:

    def __init__(self):
        self.crc16_tab_calculated: bool = False
        self.crc16_tab = []

    def calculate_crc16(self, input_data: bytes) -> int:
        crc: int = CRC_START_16

        if not self.crc16_tab_calculated:
            self.init_crc16_tab()

        for byte in input_data:
            short_c = 0x00FF & byte
            tmp = crc ^ short_c
            crc = (crc >> 8) ^ self.crc16_tab[tmp & 0xff]

        return crc & 0xffff

    def init_crc16_tab(self):
        for i in range(256):
            crc = 0
            c = i
            for j in range(8):
                if (crc ^ c) & 0x0001:
                    crc = (crc >> 1) ^ CRC_POLY_16
                else:
                    crc = crc >> 1

                c = c >> 1

            self.crc16_tab.append(crc)

        self.crc16_tab_calculated = True
