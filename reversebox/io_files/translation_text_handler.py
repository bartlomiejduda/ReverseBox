"""
Copyright © 2023  Bartłomiej Duda
License: GPL-3.0 License
"""

import logging
from dataclasses import dataclass

# mypy: ignore-errors
from datetime import datetime, timezone
from typing import Callable, List, Optional

import polib

from reversebox.common.logger import get_logger
from reversebox.io_files.bytes_handler import BytesHandler
from reversebox.io_files.file_handler import FileHandler

logger = get_logger(__name__)


@dataclass
class TranslationEntry:
    text_offset: int
    text_export_length: int
    text_import_length: Optional[int] = None
    text_export_transform_function: Optional[Callable[[bytes], bytes]] = None
    text_import_transform_function: Optional[Callable[[bytes], bytes]] = None
    text_key: Optional[str] = None


class TranslationTextHandler(FileHandler):
    def __init__(
        self,
        translation_memory: List[TranslationEntry],
        file_path: str,
        endianess_str: str = "little",
        global_export_function: Optional[Callable[[bytes], bytes]] = None,
        global_import_function: Optional[Callable[[bytes], bytes]] = None,
        log_level: int = logging.WARNING,
    ):
        self.translation_memory: List[TranslationEntry] = translation_memory
        self.global_export_function: Optional[Callable[[bytes], bytes]] = (
            global_export_function
        )
        self.global_import_function: Optional[Callable[[bytes], bytes]] = (
            global_import_function
        )
        logger.setLevel(log_level)
        super(TranslationTextHandler, self).__init__(file_path, "rb", endianess_str)

    def _get_current_utc_datetime_for_po_file(self) -> str:
        current_datetime: datetime = datetime.now(timezone.utc)
        return current_datetime.strftime("%d/%m/%Y %H:%M:%S")

    def export_all_text(
        self,
        output_po_file_path: str,
        language: str = "pl",
        key: str = "text_to_translate_",
        creation_date_string: str = None,
        revision_date_string: str = None,
        encoding: str = "utf8",
    ) -> bool:
        self.open_mode = "rb"
        self.open()
        entries_count: int = 0
        binary_total_file_size: int = self.get_file_size()
        output_po_file = polib.POFile(encoding=encoding)
        output_po_file.metadata = {
            "Project-Id-Version": "1.0",
            "Report-Msgid-Bugs-To": "you@example.com",
            "POT-Creation-Date": (
                creation_date_string
                if creation_date_string
                else self._get_current_utc_datetime_for_po_file()
            ),
            "PO-Revision-Date": (
                revision_date_string
                if revision_date_string
                else self._get_current_utc_datetime_for_po_file()
            ),
            "Last-Translator": "you <you@example.com>",
            "Language-Team": "English <yourteam@example.com>",
            "Language": language,
            "MIME-Version": "1.0",
            "Content-Type": f"text/plain; charset={encoding}",
        }

        for translation_entry in self.translation_memory:
            entries_count += 1
            if translation_entry.text_offset >= binary_total_file_size:
                logger.error(
                    f"Wrong offset: {translation_entry.text_offset}. "
                    f"It's larger than binary total size."
                )
                self.close()
                return False
            if (
                translation_entry.text_offset + translation_entry.text_export_length
            ) > binary_total_file_size:
                logger.error(
                    f"Wrong str length for str at offset: {translation_entry.text_offset}."
                    f"It's larger than binary total size."
                )
                self.close()
                return False
            self.seek(translation_entry.text_offset)
            text_entry_key: str = key + str(entries_count)  # default key
            if translation_entry.text_key:
                text_entry_key = translation_entry.text_key  # user defined key
            text_entry_bytes: bytes = self.read_bytes(
                translation_entry.text_export_length
            )
            if translation_entry.text_export_transform_function:
                text_entry_bytes = translation_entry.text_export_transform_function(
                    text_entry_bytes
                )
            elif self.global_export_function:
                text_entry_bytes = self.global_export_function(text_entry_bytes)
            else:
                logger.info("No export function for this entry...")
            try:
                text_entry_str: str = text_entry_bytes.decode(encoding)
            except Exception as error:
                logger.error(
                    f"Couldn't decode entry at offset {translation_entry.text_offset}. "
                    f"Error: {error}"
                )
                self.close()
                return False

            comment_text: str = (
                f"text_offset={translation_entry.text_offset} | "
                f"export_length={translation_entry.text_export_length} | "
                f"import_length={translation_entry.text_import_length}"
            )

            output_po_file.append(
                polib.POEntry(
                    msgctxt=text_entry_key,
                    msgid=text_entry_str,
                    msgstr="",
                    comment=comment_text,
                )
            )
        try:
            output_po_file.save(output_po_file_path)
        except Exception:
            logger.error(f"Couldn't save po file to path: {output_po_file_path}")
            self.close()
            return False

        self.close()
        return True

    def import_all_text(
        self,
        input_po_file_path,
        encoding: str = "utf8",
        create_backup_file: bool = True,
    ) -> bool:
        self.open_mode = "rb"
        self.open()
        import_file_whole_file_content: bytes = self.read_whole_file_content()
        self.close()

        if create_backup_file:
            backup_file_path = self.file_path + ".backup"
            logger.info(f"Creating backup file at path: {backup_file_path}")
            try:
                backup_file = open(backup_file_path, "wb")
                backup_file.write(import_file_whole_file_content)
                backup_file.close()
                logger.info(
                    f"Successfully created backup file at path: {backup_file_path}"
                )
            except Exception as error:
                logger.error(f"Error occurred while creating backup file: {error}")

        self.open_mode = "wb"
        self.open()
        self.write_bytes(import_file_whole_file_content)

        try:
            input_po_file = polib.pofile(input_po_file_path, encoding=encoding)
        except Exception:
            logger.error(f"Couldn't load PO file from path: {input_po_file_path}")
            return False

        for po_entry, memory_entry in zip(input_po_file, self.translation_memory):
            translated_text: str = po_entry.msgstr
            if memory_entry.text_import_length:
                import_length: int = memory_entry.text_import_length
            else:
                import_length: int = memory_entry.text_export_length

            import_bytes: bytes = translated_text.encode(encoding)
            if memory_entry.text_import_transform_function:
                import_bytes = memory_entry.text_import_transform_function(import_bytes)
            elif self.global_import_function:
                import_bytes = self.global_import_function(import_bytes)
            else:
                logger.info("No import function for this entry")

            bytes_length: int = len(import_bytes)

            if bytes_length > import_length:
                logger.warning(
                    f'[WARN] String "{translated_text}" after conversion to bytes is longer '
                    f"than expected import length {import_length}, so it was automatically trimmed."
                )
                bytes_handler = BytesHandler(import_bytes)
                import_bytes = bytes_handler.get_bytes(0, import_length)
            elif bytes_length < import_length:
                bytes_handler = BytesHandler(import_bytes)
                import_bytes = bytes_handler.fill_to_length(import_length)

            self.seek(memory_entry.text_offset)
            self.write_bytes(import_bytes)

        self.close()
        return True


def generate_translation_entries(
    txt_file_path: str, text_key: str = "text_to_translate"
) -> bool:
    """
    This function should be used along with "strings" program from SysInternals https://learn.microsoft.com/en-us/sysinternals/downloads/strings
    First, you should generate text dump using command "strings64.exe -o <binary_file_path> > <output_path>.
    Then you should search for text entries in the dump and copy them to some output file e.g. "entries.txt"
    Then you just need to run this function with your "entries.txt" as an input parameter for this function.
    """
    try:
        txt_file = open(txt_file_path, "rt")
    except Exception as error:
        logger.error(f"Error with opening file: {error}")
        return False

    for line in txt_file:
        line = line.strip()
        offset = line.split(":")[0]
        text = line.split(":")[-1]
        output_entry = f'\tTranslationEntry(text_offset={offset}, text_export_length={len(text)}, text_key="{text_key}"),'
        print(output_entry)

    return True


def check_translation_entries(
    translation_memory_to_check: List[TranslationEntry],
) -> bool:
    """
    Default function for checking if entries in Translation Memory are correct.
    """
    check_offsets_list: List[int] = []

    for translation_entry in translation_memory_to_check:
        if translation_entry.text_offset in check_offsets_list:
            logger.error(f"Duplicated text_offset: {translation_entry.text_offset}")
            return False

        if (
            translation_entry.text_import_length
            and translation_entry.text_import_length
            < translation_entry.text_export_length
        ):
            logger.error(
                f"Import length is lower than export length for entry with offset {translation_entry.text_offset}"
            )
            return False

        check_offsets_list.append(translation_entry.text_offset)
    return True


windows_1250_pl_no_accents_character_mapping: dict = {
    b"\xAF": b"\x5A",  # Ż -> Z
    b"\xD3": b"\x4F",  # Ó -> O
    b"\xA3": b"\x4C",  # Ł -> L
    b"\xC6": b"\x43",  # Ć -> C
    b"\xCA": b"\x45",  # Ę -> E
    b"\x8C": b"\x53",  # Ś -> S
    b"\xA5": b"\x41",  # Ą -> A
    b"\x8F": b"\x5A",  # Ź -> Z
    b"\xD1": b"\x4E",  # Ń -> N
    b"\xBF": b"\x7A",  # ż -> z
    b"\xF3": b"\x6F",  # ó -> o
    b"\xB3": b"\x6C",  # ł -> l
    b"\xE6": b"\x63",  # ć -> c
    b"\xEA": b"\x65",  # ę -> e
    b"\x9C": b"\x73",  # ś -> s
    b"\xB9": b"\x61",  # ą -> a
    b"\x9F": b"\x7A",  # ź -> z
    b"\xF1": b"\x6E",  # ń -> n
}
