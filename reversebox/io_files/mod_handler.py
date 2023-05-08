"""
Copyright © 2023  Bartłomiej Duda
License: GPL-3.0 License
"""

import logging
import os
from dataclasses import dataclass
from typing import List

from reversebox.common.logger import get_logger
from reversebox.io_files.bytes_handler import BytesHandler
from reversebox.io_files.file_handler import FileHandler

logger = get_logger(__name__)


@dataclass
class ModEntry:
    file_offset: int
    file_size: int
    file_relative_path: str


class ModHandler(FileHandler):
    def __init__(
        self,
        mod_memory: List[ModEntry],
        archive_file_path: str,
        log_level: int = logging.WARNING,
    ):
        self.mod_memory: List[ModEntry] = mod_memory
        logger.setLevel(log_level)
        super(ModHandler, self).__init__(archive_file_path, "rb")

    def export_all_files(
        self,
        output_directory: str,
    ) -> bool:
        self.open_mode = "rb"
        self.open()
        binary_total_file_size: int = self.get_file_size()

        for file_entry in self.mod_memory:
            if file_entry.file_offset > binary_total_file_size:
                logger.error(
                    f"File offset {file_entry.file_offset} is larger than archive size."
                )
                return False
            if (file_entry.file_offset + file_entry.file_size) > binary_total_file_size:
                logger.error(
                    f"File end offset {(file_entry.file_offset + file_entry.file_size)} "
                    f"is larger than archive EOF."
                )
                return False

            full_file_output_path: str = os.path.join(
                os.sep, output_directory, file_entry.file_relative_path
            )

            if not os.path.exists(os.path.dirname(full_file_output_path)):
                try:
                    os.makedirs(os.path.dirname(full_file_output_path))
                except FileNotFoundError:
                    logger.error(
                        f"Couldn't create output directory: {full_file_output_path}"
                    )
                    return False

            try:
                output_file = open(full_file_output_path, "wb")
            except Exception as error:
                logger.error(
                    f"Couldn't save file at path: {file_entry.file_relative_path}. Error: {error}"
                )
                return False

            self.seek(file_entry.file_offset)
            file_data: bytes = self.read_bytes(file_entry.file_size)
            output_file.write(file_data)
            output_file.close()
            logger.info(f"File {file_entry.file_relative_path} has been extracted.")

        self.close()
        return True

    def import_all_files(
        self,
        output_directory: str,
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
                return False

        self.open_mode = "wb"
        self.open()
        self.write_bytes(import_file_whole_file_content)

        for memory_entry in self.mod_memory:
            full_memory_file_path: str = os.path.join(
                output_directory, memory_entry.file_relative_path
            )
            try:
                memory_file = open(full_memory_file_path, "rb")
            except Exception as error:
                logger.error(f"Couldn't open memory file. Error: {error}")
                return False

            memory_file_data: bytes = memory_file.read()
            memory_file_data_size: int = len(memory_file_data)

            if memory_file_data_size > memory_entry.file_size:
                logger.warning(
                    f'[WARN] File at path "{memory_entry.file_relative_path}" is larger '
                    f"than expected file size {memory_entry.file_size}, so it was automatically trimmed."
                )
                bytes_handler = BytesHandler(memory_file_data)
                memory_file_data = bytes_handler.get_bytes(0, memory_entry.file_size)
            elif memory_file_data_size < memory_entry.file_size:
                bytes_handler = BytesHandler(memory_file_data)
                memory_file_data = bytes_handler.fill_to_length(memory_entry.file_size)

            self.seek(memory_entry.file_offset)
            self.write_bytes(memory_file_data)

        self.close()
        return True
