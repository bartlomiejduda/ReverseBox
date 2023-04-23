"""
Copyright © 2023  Bartłomiej Duda
License: GPL-3.0 License
"""
import os
from typing import List

import pytest

from reversebox.io_files.translation_text_handler import (
    TranslationEntry,
    TranslationTextHandler,
)

fake_character_mapping: dict = {
    b"\xC5\xBB": b"\x5A",  # Ż -> Z
    b"\xC3\xB3": b"\x6F",  # ó -> o
    b"\xC5\x82": b"\x6C",  # ł --> l
}


def fake_import_transform(input_bytes: bytes) -> bytes:
    for key, value in fake_character_mapping.items():
        input_bytes = input_bytes.replace(key, value)
    return input_bytes


# fmt: off
translation_memory: List[TranslationEntry] = [
    TranslationEntry(text_offset=35, text_export_length=9),
    TranslationEntry(text_offset=97, text_export_length=9),
    TranslationEntry(text_offset=107, text_export_length=7),
    TranslationEntry(text_offset=115, text_export_length=4),
    TranslationEntry(text_offset=157, text_export_length=42),
    TranslationEntry(text_offset=224, text_export_length=33),
    TranslationEntry(text_offset=315, text_export_length=9),
    TranslationEntry(text_offset=342, text_export_length=10),
    TranslationEntry(text_offset=411, text_export_length=9),
    TranslationEntry(text_offset=422, text_export_length=9),
    TranslationEntry(text_offset=434, text_export_length=12),
    TranslationEntry(text_offset=452, text_export_length=13, text_import_length=17,
                     text_import_transform_function=fake_import_transform),
]
# fmt: on


@pytest.mark.unittest
def test_translation_text_handler_extract_all_text():
    binary_file_path = os.path.join(
        os.path.dirname(__file__), "data/fake_file8_translation_before.bin"
    )
    po_file_path = os.path.join(
        os.path.dirname(__file__), "data\\fake_file8_translation_before.po"
    )
    translation_handler = TranslationTextHandler(
        translation_memory=translation_memory, file_path=binary_file_path
    )
    result = translation_handler.export_all_text(po_file_path)
    assert result


@pytest.mark.unittest
def test_translation_text_handler_import_all_text():
    binary_file_path = os.path.join(
        os.path.dirname(__file__), "data\\fake_file8_translation_after.bin"
    )
    po_file_path = os.path.join(
        os.path.dirname(__file__), "data\\fake_file8_translation_after.po"
    )
    translation_handler = TranslationTextHandler(
        translation_memory=translation_memory, file_path=binary_file_path
    )
    result = translation_handler.import_all_text(po_file_path)
    assert result
    assert os.path.getsize(binary_file_path) == 500
