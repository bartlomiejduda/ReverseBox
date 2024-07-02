"""
Copyright © 2022-2024  Bartłomiej Duda
License: GPL-3.0 License
"""
import os.path


def convert_int_to_hex_string(input_value: int) -> str:
    return "0x%02X" % int(input_value)


def convert_hex_string_to_int(input_string: str) -> int:
    return int(input_string, 16)


def calculate_padding_length(input_length: int, div: int) -> int:
    return (div - (input_length % div)) % div


def get_length_with_padding(input_length: int, div: int):
    padding_length: int = calculate_padding_length(input_length, div)
    return input_length + padding_length


def convert_bits_str_to_int(input_bits_str: str) -> int:
    return int(input_bits_str, 2)


def convert_int_to_bool(input_number: int) -> bool:
    return bool(input_number)


# e.g. "file.dds" --> DDS
def get_file_extension(input_filename: str) -> str:
    return os.path.splitext(input_filename)[-1].strip(".").upper()
