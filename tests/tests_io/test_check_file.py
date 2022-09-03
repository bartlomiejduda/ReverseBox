"""
Copyright © 2022  Bartłomiej Duda
License: GPL-3.0 License
"""
import os

import pytest

from reversebox.io_files.check_file import check_file


@pytest.mark.unittest
def test_check_file_to_match_expected_result():
    file_path = os.path.join(os.path.dirname(__file__), "data\\fake_file1.xml")
    code, status = check_file(file_path, ".XML", False)
    assert code == "OK"

    file_path = os.path.join(os.path.dirname(__file__), "data\\fake_file2.txt")
    code, status = check_file(file_path, ".TXT", False)
    assert code == "OK"

    file_path = os.path.join(os.path.dirname(__file__), "data\\fake_file2.txt")
    code, status = check_file(file_path, ".XXX", False)
    assert code != "OK"
