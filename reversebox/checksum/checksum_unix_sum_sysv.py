"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

# https://en.wikipedia.org/wiki/Sum_(Unix)
# https://en.wikipedia.org/wiki/SYSV_checksum


class UnixSumSysVHandler:
    def __init__(self):
        pass

    def calculate_unix_sum_sysv(self, input_data: bytes) -> int:
        s = 0
        for input_byte in input_data:
            s += input_byte & 0xFF
        r = (s & 0xFFFF) + ((s & 0xFFFFFFFF) >> 16) & 0xFFFFFFFF
        checksum = (r & 0xFFFF) + (r >> 16) & 0xFFFFFFFF
        return checksum
