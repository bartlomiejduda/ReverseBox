"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import pytest

from reversebox.compression.compression_jcalg1 import JCALG1Handler


@pytest.mark.unittest
def test_open_and_compress_file_with_jcalg1():
    # TODO - this test needs to be rewritten...
    test_data = b"ABCD"
    jcalg1_handler = JCALG1Handler()
    with pytest.raises(Exception, match="Not supported yet!"):
        jcalg1_handler.compress_data(test_data)
    assert True
