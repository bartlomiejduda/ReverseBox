"""
Copyright © 2022  Bartłomiej Duda
License: GPL-3.0 License
"""


def convert_int_to_hex_string(input_checksum: int) -> str:
    return "0x%02X" % int(input_checksum)


def convert_hex_string_to_int(input_string: str) -> int:
    return int(input_string, 16)
