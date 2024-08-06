"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""
import pytest

from reversebox.io_files.bytes_helper_functions import get_bits
from tests.common import GetBitsTestEntry

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
        GetBitsTestEntry(value_to_test=171, number_of_bits=5, position=2, expected_result=10)
    ]

    for test_entry in get_bits_data_list:
        result: int = get_bits(test_entry.value_to_test, test_entry.number_of_bits, test_entry.position)
        assert result == test_entry.expected_result
