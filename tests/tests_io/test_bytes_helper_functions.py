"""
Copyright © 2024-2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import io

import pytest

from reversebox.io_files.bytes_helper_functions import (
    get_bits,
    get_bits_string,
    get_int8,
    get_int16,
    get_int24,
    get_int32,
    get_int48,
    get_int64,
    get_uint8,
    get_uint16,
    get_uint24,
    get_uint32,
    get_uint48,
    get_uint64,
    set_int8,
    set_int16,
    set_int24,
    set_int32,
    set_int48,
    set_int64,
    set_uint8,
    set_uint16,
    set_uint24,
    set_uint32,
    set_uint48,
    set_uint64,
)
from tests.common import GetBitsStringTestEntry, GetBitsTestEntry, GetSetBytesEntry

# fmt: off


@pytest.mark.unittest
def test_bytes_helper_functions_get_bits():
    get_bits_data_list = [
        GetBitsTestEntry(value_to_test=134217728, number_of_bits=3, position=27, expected_result=1),  # DTEX RGB565 pixel format flag
        GetBitsTestEntry(value_to_test=402653184, number_of_bits=3, position=27, expected_result=3),  # DTEX VUV422 pixel format flag
        GetBitsTestEntry(value_to_test=17, number_of_bits=3, position=0, expected_result=1),
        GetBitsTestEntry(value_to_test=17, number_of_bits=6, position=0, expected_result=17),
        GetBitsTestEntry(value_to_test=2273, number_of_bits=3, position=5, expected_result=7),
        GetBitsTestEntry(value_to_test=171, number_of_bits=4, position=2, expected_result=10),  # example from https://www.iditect.com/programming/python-example/python-slicing-extract-k-bits-given-position.html
        GetBitsTestEntry(value_to_test=171, number_of_bits=5, position=2, expected_result=10),

        GetBitsTestEntry(value_to_test=528391, number_of_bits=1, position=0, expected_result=1),  # DDS file - DDSD_CAPS flag
        GetBitsTestEntry(value_to_test=528391, number_of_bits=1, position=1, expected_result=1),  # DDS file - DDSD_HEIGHT flag
        GetBitsTestEntry(value_to_test=528391, number_of_bits=1, position=2, expected_result=1),  # DDS file - DDSD_WIDTH flag
        GetBitsTestEntry(value_to_test=528391, number_of_bits=1, position=3, expected_result=0),  # DDS file - no flag
        GetBitsTestEntry(value_to_test=528391, number_of_bits=1, position=4, expected_result=0),  # DDS file - no flag
    ]

    for test_entry in get_bits_data_list:
        result: int = get_bits(test_entry.value_to_test, test_entry.number_of_bits, test_entry.position)
        assert result == test_entry.expected_result


@pytest.mark.unittest
def test_bytes_helper_functions_get_bits_string():
    get_bits_string_data_list = [
        GetBitsStringTestEntry(value_to_test=528391, bits_to_fill=32, expected_string="00000000000010000001000000000111"),  # DDS flags value
        GetBitsStringTestEntry(value_to_test=171, bits_to_fill=16, expected_string="0000000010101011"),
        GetBitsStringTestEntry(value_to_test=2273, bits_to_fill=16, expected_string="0000100011100001"),
        ]

    for test_entry in get_bits_string_data_list:
        result: str = get_bits_string(test_entry.value_to_test, test_entry.bits_to_fill)
        assert result == test_entry.expected_string


def _assert_get_set_functions(value_bytes: bytes, value_int: int, value_endianess: str, get_func, set_func) -> None:
    input_memory_file = io.BytesIO(initial_bytes=value_bytes)
    input_data: bytes = input_memory_file.read(len(value_bytes))
    input_value: int = get_func(input_data, value_endianess)
    assert input_value == value_int

    output_memory_file = io.BytesIO()
    output_value: bytes = set_func(value_int, value_endianess)
    result: int = output_memory_file.write(output_value)
    assert result == len(value_bytes)
    assert output_value == value_bytes


# 8 bits #
@pytest.mark.unittest
def test_bytes_helper_functions_get_and_set_uint8():

    get_set_test_entries_list: list = [
        GetSetBytesEntry(value_int=15, value_bytes=b"\x0F", endianess="<"),
        GetSetBytesEntry(value_int=0, value_bytes=b"\x00", endianess="<"),
        GetSetBytesEntry(value_int=2, value_bytes=b"\x02", endianess="<"),
        GetSetBytesEntry(value_int=255, value_bytes=b"\xFF", endianess="<"),

        GetSetBytesEntry(value_int=15, value_bytes=b"\x0F", endianess=">"),
        GetSetBytesEntry(value_int=0, value_bytes=b"\x00", endianess=">"),
        GetSetBytesEntry(value_int=2, value_bytes=b"\x02", endianess=">"),
        GetSetBytesEntry(value_int=255, value_bytes=b"\xFF", endianess=">")
    ]
    for test_entry in get_set_test_entries_list:
        _assert_get_set_functions(test_entry.value_bytes, test_entry.value_int, test_entry.endianess, get_uint8, set_uint8)


@pytest.mark.unittest
def test_bytes_helper_functions_get_and_set_int8():

    get_set_test_entries_list: list = [
        GetSetBytesEntry(value_int=15, value_bytes=b"\x0F", endianess="<"),
        GetSetBytesEntry(value_int=0, value_bytes=b"\x00", endianess="<"),
        GetSetBytesEntry(value_int=2, value_bytes=b"\x02", endianess="<"),
        GetSetBytesEntry(value_int=-1, value_bytes=b"\xFF", endianess="<"),
        GetSetBytesEntry(value_int=-10, value_bytes=b"\xF6", endianess="<"),
        GetSetBytesEntry(value_int=-120, value_bytes=b"\x88", endianess="<"),
        GetSetBytesEntry(value_int=127, value_bytes=b"\x7F", endianess="<"),
        GetSetBytesEntry(value_int=-128, value_bytes=b"\x80", endianess="<"),

        GetSetBytesEntry(value_int=15, value_bytes=b"\x0F", endianess=">"),
        GetSetBytesEntry(value_int=0, value_bytes=b"\x00", endianess=">"),
        GetSetBytesEntry(value_int=2, value_bytes=b"\x02", endianess=">"),
        GetSetBytesEntry(value_int=-1, value_bytes=b"\xFF", endianess=">"),
        GetSetBytesEntry(value_int=-10, value_bytes=b"\xF6", endianess=">"),
        GetSetBytesEntry(value_int=-120, value_bytes=b"\x88", endianess=">"),
        GetSetBytesEntry(value_int=127, value_bytes=b"\x7F", endianess=">"),
        GetSetBytesEntry(value_int=-128, value_bytes=b"\x80", endianess=">"),

    ]
    for test_entry in get_set_test_entries_list:
        _assert_get_set_functions(test_entry.value_bytes, test_entry.value_int, test_entry.endianess, get_int8, set_int8)


# 16 bits #
@pytest.mark.unittest
def test_bytes_helper_functions_get_and_set_uint16():

    get_set_test_entries_list: list = [
        GetSetBytesEntry(value_int=15, value_bytes=b"\x0F\x00", endianess="<"),
        GetSetBytesEntry(value_int=0, value_bytes=b"\x00\x00", endianess="<"),
        GetSetBytesEntry(value_int=2, value_bytes=b"\x02\x00", endianess="<"),
        GetSetBytesEntry(value_int=255, value_bytes=b"\xFF\x00", endianess="<"),
        GetSetBytesEntry(value_int=43690, value_bytes=b"\xAA\xAA", endianess="<"),

        GetSetBytesEntry(value_int=15, value_bytes=b"\x00\x0F", endianess=">"),
        GetSetBytesEntry(value_int=0, value_bytes=b"\x00\x00", endianess=">"),
        GetSetBytesEntry(value_int=2, value_bytes=b"\x00\x02", endianess=">"),
        GetSetBytesEntry(value_int=255, value_bytes=b"\x00\xFF", endianess=">"),
        GetSetBytesEntry(value_int=43690, value_bytes=b"\xAA\xAA", endianess=">"),
    ]
    for test_entry in get_set_test_entries_list:
        _assert_get_set_functions(test_entry.value_bytes, test_entry.value_int, test_entry.endianess, get_uint16, set_uint16)


@pytest.mark.unittest
def test_bytes_helper_functions_get_and_set_int16():

    get_set_test_entries_list: list = [
        GetSetBytesEntry(value_int=15, value_bytes=b"\x0F\x00", endianess="<"),
        GetSetBytesEntry(value_int=0, value_bytes=b"\x00\x00", endianess="<"),
        GetSetBytesEntry(value_int=2, value_bytes=b"\x02\x00", endianess="<"),
        GetSetBytesEntry(value_int=255, value_bytes=b"\xFF\x00", endianess="<"),
        GetSetBytesEntry(value_int=-21846, value_bytes=b"\xAA\xAA", endianess="<"),
        GetSetBytesEntry(value_int=-17426, value_bytes=b"\xEE\xBB", endianess="<"),
        GetSetBytesEntry(value_int=-1, value_bytes=b"\xFF\xFF", endianess="<"),

        GetSetBytesEntry(value_int=15, value_bytes=b"\x00\x0F", endianess=">"),
        GetSetBytesEntry(value_int=0, value_bytes=b"\x00\x00", endianess=">"),
        GetSetBytesEntry(value_int=2, value_bytes=b"\x00\x02", endianess=">"),
        GetSetBytesEntry(value_int=255, value_bytes=b"\x00\xFF", endianess=">"),
        GetSetBytesEntry(value_int=-21846, value_bytes=b"\xAA\xAA", endianess=">"),
        GetSetBytesEntry(value_int=-17426, value_bytes=b"\xBB\xEE", endianess=">"),
        GetSetBytesEntry(value_int=-1, value_bytes=b"\xFF\xFF", endianess=">"),
    ]
    for test_entry in get_set_test_entries_list:
        _assert_get_set_functions(test_entry.value_bytes, test_entry.value_int, test_entry.endianess, get_int16, set_int16)


# 24 bits #
@pytest.mark.unittest
def test_bytes_helper_functions_get_and_set_uint24():

    get_set_test_entries_list: list = [
        GetSetBytesEntry(value_int=15, value_bytes=b"\x0F\x00\x00", endianess="<"),
        GetSetBytesEntry(value_int=0, value_bytes=b"\x00\x00\x00", endianess="<"),
        GetSetBytesEntry(value_int=2, value_bytes=b"\x02\x00\x00", endianess="<"),
        GetSetBytesEntry(value_int=255, value_bytes=b"\xFF\x00\x00", endianess="<"),
        GetSetBytesEntry(value_int=43690, value_bytes=b"\xAA\xAA\x00", endianess="<"),

        GetSetBytesEntry(value_int=15, value_bytes=b"\x00\x00\x0F", endianess=">"),
        GetSetBytesEntry(value_int=0, value_bytes=b"\x00\x00\x00", endianess=">"),
        GetSetBytesEntry(value_int=2, value_bytes=b"\x00\x00\x02", endianess=">"),
        GetSetBytesEntry(value_int=255, value_bytes=b"\x00\x00\xFF", endianess=">"),
        GetSetBytesEntry(value_int=43690, value_bytes=b"\x00\xAA\xAA", endianess=">"),
    ]
    for test_entry in get_set_test_entries_list:
        _assert_get_set_functions(test_entry.value_bytes, test_entry.value_int, test_entry.endianess, get_uint24, set_uint24)


@pytest.mark.unittest
def test_bytes_helper_functions_get_and_set_int24():

    get_set_test_entries_list: list = [
        GetSetBytesEntry(value_int=15, value_bytes=b"\x0F\x00\x00", endianess="<"),
        GetSetBytesEntry(value_int=0, value_bytes=b"\x00\x00\x00", endianess="<"),
        GetSetBytesEntry(value_int=2, value_bytes=b"\x02\x00\x00", endianess="<"),
        GetSetBytesEntry(value_int=255, value_bytes=b"\xFF\x00\x00", endianess="<"),
        GetSetBytesEntry(value_int=-21846, value_bytes=b"\xAA\xAA\xFF", endianess="<"),
        GetSetBytesEntry(value_int=-17426, value_bytes=b"\xEE\xBB\xFF", endianess="<"),
        GetSetBytesEntry(value_int=-1, value_bytes=b"\xFF\xFF\xFF", endianess="<"),
        #
        GetSetBytesEntry(value_int=15, value_bytes=b"\x00\x00\x0F", endianess=">"),
        GetSetBytesEntry(value_int=0, value_bytes=b"\x00\x00\x00", endianess=">"),
        GetSetBytesEntry(value_int=2, value_bytes=b"\x00\x00\x02", endianess=">"),
        GetSetBytesEntry(value_int=255, value_bytes=b"\x00\x00\xFF", endianess=">"),
        GetSetBytesEntry(value_int=-21846, value_bytes=b"\xFF\xAA\xAA", endianess=">"),
        GetSetBytesEntry(value_int=-17426, value_bytes=b"\xFF\xBB\xEE", endianess=">"),
        GetSetBytesEntry(value_int=-1, value_bytes=b"\xFF\xFF\xFF", endianess=">"),
    ]

    for test_entry in get_set_test_entries_list:
        _assert_get_set_functions(test_entry.value_bytes, test_entry.value_int, test_entry.endianess, get_int24, set_int24)


# 32 bits #
@pytest.mark.unittest
def test_bytes_helper_functions_get_and_set_uint32():

    get_set_test_entries_list: list = [
        GetSetBytesEntry(value_int=15, value_bytes=b"\x0F\x00\x00\x00", endianess="<"),
        GetSetBytesEntry(value_int=0, value_bytes=b"\x00\x00\x00\x00", endianess="<"),
        GetSetBytesEntry(value_int=2, value_bytes=b"\x02\x00\x00\x00", endianess="<"),
        GetSetBytesEntry(value_int=255, value_bytes=b"\xFF\x00\x00\x00", endianess="<"),
        GetSetBytesEntry(value_int=43690, value_bytes=b"\xAA\xAA\x00\x00", endianess="<"),

        GetSetBytesEntry(value_int=15, value_bytes=b"\x00\x00\x00\x0F", endianess=">"),
        GetSetBytesEntry(value_int=0, value_bytes=b"\x00\x00\x00\x00", endianess=">"),
        GetSetBytesEntry(value_int=2, value_bytes=b"\x00\x00\x00\x02", endianess=">"),
        GetSetBytesEntry(value_int=255, value_bytes=b"\x00\x00\x00\xFF", endianess=">"),
        GetSetBytesEntry(value_int=43690, value_bytes=b"\x00\x00\xAA\xAA", endianess=">"),
    ]
    for test_entry in get_set_test_entries_list:
        _assert_get_set_functions(test_entry.value_bytes, test_entry.value_int, test_entry.endianess, get_uint32, set_uint32)


@pytest.mark.unittest
def test_bytes_helper_functions_get_and_set_int32():

    get_set_test_entries_list: list = [
        GetSetBytesEntry(value_int=15, value_bytes=b"\x0F\x00\x00\x00", endianess="<"),
        GetSetBytesEntry(value_int=0, value_bytes=b"\x00\x00\x00\x00", endianess="<"),
        GetSetBytesEntry(value_int=2, value_bytes=b"\x02\x00\x00\x00", endianess="<"),
        GetSetBytesEntry(value_int=255, value_bytes=b"\xFF\x00\x00\x00", endianess="<"),
        GetSetBytesEntry(value_int=-21846, value_bytes=b"\xAA\xAA\xFF\xFF", endianess="<"),
        GetSetBytesEntry(value_int=-17426, value_bytes=b"\xEE\xBB\xFF\xFF", endianess="<"),
        GetSetBytesEntry(value_int=-1, value_bytes=b"\xFF\xFF\xFF\xFF", endianess="<"),

        GetSetBytesEntry(value_int=15, value_bytes=b"\x00\x00\x00\x0F", endianess=">"),
        GetSetBytesEntry(value_int=0, value_bytes=b"\x00\x00\x00\x00", endianess=">"),
        GetSetBytesEntry(value_int=2, value_bytes=b"\x00\x00\x00\x02", endianess=">"),
        GetSetBytesEntry(value_int=255, value_bytes=b"\x00\x00\x00\xFF", endianess=">"),
        GetSetBytesEntry(value_int=-21846, value_bytes=b"\xFF\xFF\xAA\xAA", endianess=">"),
        GetSetBytesEntry(value_int=-17426, value_bytes=b"\xFF\xFF\xBB\xEE", endianess=">"),
        GetSetBytesEntry(value_int=-1, value_bytes=b"\xFF\xFF\xFF\xFF", endianess=">"),
    ]

    for test_entry in get_set_test_entries_list:
        _assert_get_set_functions(test_entry.value_bytes, test_entry.value_int, test_entry.endianess, get_int32, set_int32)


# 48 bits #
@pytest.mark.unittest
def test_bytes_helper_functions_get_and_set_uint48():

    get_set_test_entries_list: list = [
        GetSetBytesEntry(value_int=15, value_bytes=b"\x0F\x00\x00\x00\x00\x00", endianess="<"),
        GetSetBytesEntry(value_int=0, value_bytes=b"\x00\x00\x00\x00\x00\x00", endianess="<"),
        GetSetBytesEntry(value_int=2, value_bytes=b"\x02\x00\x00\x00\x00\x00", endianess="<"),
        GetSetBytesEntry(value_int=255, value_bytes=b"\xFF\x00\x00\x00\x00\x00", endianess="<"),
        GetSetBytesEntry(value_int=43690, value_bytes=b"\xAA\xAA\x00\x00\x00\x00", endianess="<"),

        GetSetBytesEntry(value_int=15, value_bytes=b"\x00\x00\x00\x00\x00\x0F", endianess=">"),
        GetSetBytesEntry(value_int=0, value_bytes=b"\x00\x00\x00\x00\x00\x00", endianess=">"),
        GetSetBytesEntry(value_int=2, value_bytes=b"\x00\x00\x00\x00\x00\x02", endianess=">"),
        GetSetBytesEntry(value_int=255, value_bytes=b"\x00\x00\x00\x00\x00\xFF", endianess=">"),
        GetSetBytesEntry(value_int=43690, value_bytes=b"\x00\x00\x00\x00\xAA\xAA", endianess=">"),
    ]
    for test_entry in get_set_test_entries_list:
        _assert_get_set_functions(test_entry.value_bytes, test_entry.value_int, test_entry.endianess, get_uint48, set_uint48)


@pytest.mark.unittest
def test_bytes_helper_functions_get_and_set_int48():

    get_set_test_entries_list: list = [
        GetSetBytesEntry(value_int=15, value_bytes=b"\x0F\x00\x00\x00\x00\x00", endianess="<"),
        GetSetBytesEntry(value_int=0, value_bytes=b"\x00\x00\x00\x00\x00\x00", endianess="<"),
        GetSetBytesEntry(value_int=2, value_bytes=b"\x02\x00\x00\x00\x00\x00", endianess="<"),
        GetSetBytesEntry(value_int=255, value_bytes=b"\xFF\x00\x00\x00\x00\x00", endianess="<"),
        GetSetBytesEntry(value_int=-21846, value_bytes=b"\xAA\xAA\xFF\xFF\xFF\xFF", endianess="<"),
        GetSetBytesEntry(value_int=-17426, value_bytes=b"\xEE\xBB\xFF\xFF\xFF\xFF", endianess="<"),
        GetSetBytesEntry(value_int=-1, value_bytes=b"\xFF\xFF\xFF\xFF\xFF\xFF", endianess="<"),

        GetSetBytesEntry(value_int=15, value_bytes=b"\x00\x00\x00\x00\x00\x0F", endianess=">"),
        GetSetBytesEntry(value_int=0, value_bytes=b"\x00\x00\x00\x00\x00\x00", endianess=">"),
        GetSetBytesEntry(value_int=2, value_bytes=b"\x00\x00\x00\x00\x00\x02", endianess=">"),
        GetSetBytesEntry(value_int=255, value_bytes=b"\x00\x00\x00\x00\x00\xFF", endianess=">"),
        GetSetBytesEntry(value_int=-21846, value_bytes=b"\xFF\xFF\xFF\xFF\xAA\xAA", endianess=">"),
        GetSetBytesEntry(value_int=-17426, value_bytes=b"\xFF\xFF\xFF\xFF\xBB\xEE", endianess=">"),
        GetSetBytesEntry(value_int=-1, value_bytes=b"\xFF\xFF\xFF\xFF\xFF\xFF", endianess=">"),
    ]

    for test_entry in get_set_test_entries_list:
        _assert_get_set_functions(test_entry.value_bytes, test_entry.value_int, test_entry.endianess, get_int48, set_int48)


# 64 bits #
@pytest.mark.unittest
def test_bytes_helper_functions_get_and_set_uint64():

    get_set_test_entries_list: list = [
        GetSetBytesEntry(value_int=15, value_bytes=b"\x0F\x00\x00\x00\x00\x00\x00\x00", endianess="<"),
        GetSetBytesEntry(value_int=0, value_bytes=b"\x00\x00\x00\x00\x00\x00\x00\x00", endianess="<"),
        GetSetBytesEntry(value_int=2, value_bytes=b"\x02\x00\x00\x00\x00\x00\x00\x00", endianess="<"),
        GetSetBytesEntry(value_int=255, value_bytes=b"\xFF\x00\x00\x00\x00\x00\x00\x00", endianess="<"),
        GetSetBytesEntry(value_int=43690, value_bytes=b"\xAA\xAA\x00\x00\x00\x00\x00\x00", endianess="<"),

        GetSetBytesEntry(value_int=15, value_bytes=b"\x00\x00\x00\x00\x00\x00\x00\x0F", endianess=">"),
        GetSetBytesEntry(value_int=0, value_bytes=b"\x00\x00\x00\x00\x00\x00\x00\x00", endianess=">"),
        GetSetBytesEntry(value_int=2, value_bytes=b"\x00\x00\x00\x00\x00\x00\x00\x02", endianess=">"),
        GetSetBytesEntry(value_int=255, value_bytes=b"\x00\x00\x00\x00\x00\x00\x00\xFF", endianess=">"),
        GetSetBytesEntry(value_int=43690, value_bytes=b"\x00\x00\x00\x00\x00\x00\xAA\xAA", endianess=">"),
    ]
    for test_entry in get_set_test_entries_list:
        _assert_get_set_functions(test_entry.value_bytes, test_entry.value_int, test_entry.endianess, get_uint64, set_uint64)


@pytest.mark.unittest
def test_bytes_helper_functions_get_and_set_int64():

    get_set_test_entries_list: list = [
        GetSetBytesEntry(value_int=15, value_bytes=b"\x0F\x00\x00\x00\x00\x00\x00\x00", endianess="<"),
        GetSetBytesEntry(value_int=0, value_bytes=b"\x00\x00\x00\x00\x00\x00\x00\x00", endianess="<"),
        GetSetBytesEntry(value_int=2, value_bytes=b"\x02\x00\x00\x00\x00\x00\x00\x00", endianess="<"),
        GetSetBytesEntry(value_int=255, value_bytes=b"\xFF\x00\x00\x00\x00\x00\x00\x00", endianess="<"),
        GetSetBytesEntry(value_int=-21846, value_bytes=b"\xAA\xAA\xFF\xFF\xFF\xFF\xFF\xFF", endianess="<"),
        GetSetBytesEntry(value_int=-17426, value_bytes=b"\xEE\xBB\xFF\xFF\xFF\xFF\xFF\xFF", endianess="<"),
        GetSetBytesEntry(value_int=-1, value_bytes=b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF", endianess="<"),

        GetSetBytesEntry(value_int=15, value_bytes=b"\x00\x00\x00\x00\x00\x00\x00\x0F", endianess=">"),
        GetSetBytesEntry(value_int=0, value_bytes=b"\x00\x00\x00\x00\x00\x00\x00\x00", endianess=">"),
        GetSetBytesEntry(value_int=2, value_bytes=b"\x00\x00\x00\x00\x00\x00\x00\x02", endianess=">"),
        GetSetBytesEntry(value_int=255, value_bytes=b"\x00\x00\x00\x00\x00\x00\x00\xFF", endianess=">"),
        GetSetBytesEntry(value_int=-21846, value_bytes=b"\xFF\xFF\xFF\xFF\xFF\xFF\xAA\xAA", endianess=">"),
        GetSetBytesEntry(value_int=-17426, value_bytes=b"\xFF\xFF\xFF\xFF\xFF\xFF\xBB\xEE", endianess=">"),
        GetSetBytesEntry(value_int=-1, value_bytes=b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF", endianess=">"),
    ]

    for test_entry in get_set_test_entries_list:
        _assert_get_set_functions(test_entry.value_bytes, test_entry.value_int, test_entry.endianess, get_int64, set_int64)
