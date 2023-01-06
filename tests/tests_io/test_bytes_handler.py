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
