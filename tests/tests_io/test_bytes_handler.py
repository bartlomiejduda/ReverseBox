"""
Copyright © 2023  Bartłomiej Duda
License: GPL-3.0 License
"""
import pytest

from reversebox.io_files.bytes_handler import BytesHandler


@pytest.mark.unittest
def test_bytes_handler_get_bytes():
    bytes_handler = BytesHandler(b"\x01\x02\x03\x04")
    test_bytes = bytes_handler.get_bytes(1, 2)

    assert test_bytes == b"\x02\x03"


@pytest.mark.unittest
def test_bytes_handler_get_bits():
    bytes_handler = BytesHandler(b"\x01\x02\x03\x04")
    result = bytes_handler.get_int_from_bits(35345345, 16, 8)

    # TODO - adjust this assert
    assert result


@pytest.mark.unittest
def test_bytes_handler_fill_to_length():
    bytes_handler = BytesHandler(b"\x01\x02\x03\x04")

    test_bytes = bytes_handler.fill_to_length(5)
    assert test_bytes == b"\x01\x02\x03\x04\x00"
    assert len(test_bytes) == 5

    test_bytes = bytes_handler.fill_to_length(6, b"\xFF")
    assert test_bytes == b"\x01\x02\x03\x04\xFF\xFF"
    assert len(test_bytes) == 6

    test_bytes = bytes_handler.fill_to_length(7)
    assert test_bytes == b"\x01\x02\x03\x04\x00\x00\x00"
    assert len(test_bytes) == 7

    with pytest.raises(Exception):
        bytes_handler.fill_to_length(5, b"\x00\x01\x02")

    with pytest.raises(Exception):
        bytes_handler.fill_to_length(1)
