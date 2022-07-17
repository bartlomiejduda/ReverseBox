CRC_START_DNP = 0x0000
CRC_POLY_DNP = 0xA6BC


# TODO - correct this
class CRC16DNPHandler:

    def __init__(self):
        self.crc16_dnp_tab_calculated: bool = False
        self.crc16_dnp_tab = []

    def calculate_crc16_dnp(self, input_data: bytes) -> int:
        crc: int = CRC_START_DNP

        if not self.crc16_dnp_tab_calculated:
            self.init_crc16_dnp_tab()

        for byte in input_data:
            short_c = 0x00FF & byte
            tmp = crc ^ short_c
            crc = (crc >> 8) ^ self.crc16_dnp_tab[tmp & 0xff]

        crc = ~crc
        low_byte = (crc & 0xff00) >> 8
        high_byte = (crc & 0x00ff) << 8
        crc = low_byte | high_byte
        return crc

    def init_crc16_dnp_tab(self):
        for i in range(256):
            crc = 0
            c = i
            for j in range(8):
                if (crc ^ c) & 0x0001:
                    crc = (crc >> 1) ^ CRC_POLY_DNP
                else:
                    crc = crc >> 1

                c = c >> 1

            self.crc16_dnp_tab.append(crc)

        self.crc16_dnp_tab_calculated = True
