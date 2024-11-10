"""
Copyright © 2022-2024  Bartłomiej Duda
License: GPL-3.0 License
"""
import os.path
from pathlib import Path


def convert_int_to_hex_string(input_value: int) -> str:
    return "0x%02X" % int(input_value)


def convert_hex_string_to_int(input_string: str) -> int:
    return int(input_string, 16)


def calculate_padding_length(input_length: int, div: int) -> int:
    return (div - (input_length % div)) % div


def get_length_with_padding(input_length: int, div: int):
    padding_length: int = calculate_padding_length(input_length, div)
    return input_length + padding_length


# e.g. "aaa" and 2 --> "aaa\x00\x00"
def fill_data_with_padding(input_data: bytes, padding_length: int) -> bytes:
    for i in range(padding_length):
        input_data += b"\x00"
    return input_data


# e.g. "aaa" and 5 --> "aaa\x00\x00"
def fill_data_with_padding_to_desired_length(
    input_data: bytes, desired_padding_length: int
):
    if len(input_data) > desired_padding_length:
        raise Exception("Data too big or desired padding too low!")
    elif len(input_data) == desired_padding_length:
        return input_data

    padding_length: int = desired_padding_length - len(input_data)
    return fill_data_with_padding(input_data, padding_length)


def convert_bits_str_to_int(input_bits_str: str) -> int:
    return int(input_bits_str, 2)


def convert_int_to_bool(input_number: int) -> bool:
    return bool(input_number)


# e.g. "file.dds" --> ".dds"
def get_file_extension(input_filename: str) -> str:
    return os.path.splitext(input_filename)[-1]


# e.g. "file.dds" --> DDS
def get_file_extension_uppercase(input_filename: str) -> str:
    return os.path.splitext(input_filename)[-1].strip(".").upper()


def get_dll_path(dll_name: str) -> str:
    dll_path: str = str(
        Path(__file__).parents[1].resolve().joinpath("libs").joinpath(dll_name)
    )
    return dll_path
