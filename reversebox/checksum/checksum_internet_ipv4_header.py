"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""


class InternetIPv4headerChecksumHandler:
    def __init__(self):
        pass

    def calculate_internet_ipv4_header_checksum(self, input_data: bytes) -> int:
        checksum = 0
        pointer = 0
        data_size = len(input_data)

        while data_size > 1:
            checksum += input_data[pointer] + (input_data[pointer + 1] << 8)
            data_size -= 2
            pointer += 2

        if data_size:  # when data size is odd
            checksum += input_data[pointer]

        checksum = (checksum >> 16) + (checksum & 0xFFFF)
        checksum += checksum >> 16

        return (~checksum) & 0xFFFF
