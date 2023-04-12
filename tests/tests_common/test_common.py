"""
Copyright © 2023  Bartłomiej Duda
License: GPL-3.0 License
"""

import pytest

from reversebox.common.common import calculate_padding_length
from tests.common import PaddingTestEntry

# fmt: off


@pytest.mark.unittest
def test_common_calculate_padding():
    padding_data_list = [
        PaddingTestEntry(test_offset=10060, test_div=2048, expected_padding=180),
    ]
    for padding_entry in padding_data_list:
        test_result = calculate_padding_length(padding_entry.test_offset, padding_entry.test_div)
        assert test_result == padding_entry.expected_padding

# fmt: on
