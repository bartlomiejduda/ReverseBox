"""
Copyright © 2023  Bartłomiej Duda
License: GPL-3.0 License
"""


class BSD16Handler:
    def __init__(self):
        pass

    def calculate_bsd16(self, input_data: bytes) -> int:
        checksum = 0
        for byte in input_data:
            checksum = (checksum >> 1) + ((checksum & 1) << 15)
            checksum += byte
            checksum &= 0xFFFF
        return checksum
