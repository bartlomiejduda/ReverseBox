"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

import pytest

from reversebox.io_files.bytes_helper_functions import get_bits, get_bits_string
from tests.common import GetBitsStringTestEntry, GetBitsTestEntry

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
