"""
Copyright © 2023-2024  Bartłomiej Duda
License: GPL-3.0 License
"""

# mypy: ignore-errors
# fmt: off

import os
from io import BufferedReader
from typing import Optional

from reversebox.common.logger import get_logger
from reversebox.io_files.bytes_helper_functions import (
    get_int8,
    get_int16,
    get_int24,
    get_int32,
    get_int64,
    get_uint8,
    get_uint16,
    get_uint24,
    get_uint32,
    get_uint64,
    set_int8,
    set_int16,
    set_int24,
    set_int32,
    set_int64,
    set_uint8,
    set_uint16,
    set_uint24,
    set_uint32,
    set_uint64,
)

logger = get_logger(__name__)


class FileHandler:
    def __init__(self, file_path: str, open_mode: str, endianess_str: str = "little"):
        self.file_path = file_path
        self.open_mode = open_mode
        self.endianess = self._get_endianess(endianess_str)

        self.file: Optional[BufferedReader] = None
        self.open()

    def open(self) -> bool:
        error_message = "File can't be opened!"
        if "r" in self.open_mode:
            if not self.check_if_file_is_readable():
                raise Exception(error_message)
        if "w" in self.open_mode:
            if not self.check_if_file_is_writable():
                raise Exception(error_message)

        try:
            self.file = open(self.file_path, self.open_mode)
        except OSError as error:
            error_message += " Error: " + str(error)
            logger.error(error_message)
            raise Exception(error_message)

        if not self.file:
            logger.error(error_message)
            raise Exception(error_message)
        return True

    def close(self) -> bool:
        self.file.close()
        return True

    def _check_file(self):
        if not self.file:
            error_message = "File is not opened!"
            logger.error(error_message)
            raise Exception(error_message)

    def _get_endianess(self, endianess: str) -> str:
        if endianess.lower() == "little":
            return "<"
        elif endianess.lower() == "big":
            return ">"
        else:
            error_message = (
                'Wrong endianess specified. Allowed values are "little" and "big".'
            )
            logger.error(error_message)
            raise Exception(error_message)

    def change_endianess(self, endianess: str):
        if endianess.lower() == "little":
            self.endianess = "<"
        elif endianess.lower() == "big":
            self.endianess = ">"
        else:
            error_message = (
                'Wrong endianess specified. Allowed values are "little" and "big".'
            )
            logger.error(error_message)
            raise Exception(error_message)

    def _check_read_mode(self) -> bool:
        if "r" not in self.open_mode:
            error_message = 'Wrong file open mode! You need to specify one of the "read" open modes!'
            logger.error(error_message)
            raise Exception(error_message)
        return True

    def check_if_file_is_readable(self) -> bool:
        if not os.access(self.file_path, os.R_OK):
            error_message = "Can't read from this file!"
            logger.error(error_message)
            raise Exception(error_message)
        return True

    def _check_write_mode(self) -> bool:
        if "w" not in self.open_mode and "a" not in self.open_mode:
            error_message = 'Wrong file open mode! You need to specify one of the "write" open modes!'
            logger.error(error_message)
            raise Exception(error_message)
        return True

    def check_if_file_is_writable(self) -> bool:
        if os.path.exists(self.file_path):
            if os.path.isfile(self.file_path):
                return os.access(self.file_path, os.W_OK)
            else:
                return False
        pdir = os.path.dirname(self.file_path)
        if not pdir:
            pdir = "."
        return os.access(pdir, os.W_OK)

    def seek(self, seek_value, seek_type: int = 0):
        # 0 = SEEK_SET (from file start)
        # 1 = SEEK_CUR (from current offset)
        # 2 = SEEK_END (from file end)
        self._check_file()
        self.file.seek(seek_value, seek_type)

    def get_position(self) -> int:
        self._check_file()
        return self.file.tell()

    def savepos(self) -> int:  # alias for quickbms compatibility
        return self.get_position()

    def get_file_size(self) -> int:
        current_position = self.get_position()
        self.seek(0, 2)
        end_of_file_position = self.get_position()
        self.seek(current_position, 0)
        return end_of_file_position

    def read_str(self, str_length: int, encoding: str = "utf8") -> str:
        self._check_file()
        self._check_read_mode()
        data = self.file.read(str_length)
        return data.decode(encoding)

    def read_bytes(self, number_of_bytes: int) -> bytes:
        self._check_file()
        self._check_read_mode()
        data = self.file.read(number_of_bytes)
        return data

    def read_whole_file_content(self) -> bytes:
        self._check_file()
        self._check_read_mode()
        current_position = self.get_position()
        self.seek(0)
        data = self.file.read()
        self.seek(current_position)
        return data

    def read_int8(self) -> int:
        self._check_file()
        data = self.file.read(1)
        return get_int8(data, self.endianess)

    def read_uint8(self) -> int:
        self._check_file()
        self._check_read_mode()
        data = self.file.read(1)
        return get_uint8(data, self.endianess)

    def read_int16(self) -> int:
        self._check_file()
        self._check_read_mode()
        data = self.file.read(2)
        return get_int16(data, self.endianess)

    def read_uint16(self) -> int:
        self._check_file()
        self._check_read_mode()
        data = self.file.read(2)
        return get_uint16(data, self.endianess)

    def read_int24(self) -> int:
        self._check_file()
        self._check_read_mode()
        data = self.file.read(4)
        return get_int24(data, self.endianess)

    def read_uint24(self) -> int:
        self._check_file()
        self._check_read_mode()
        data = self.file.read(4)
        return get_uint24(data, self.endianess)

    def read_int32(self) -> int:
        self._check_file()
        self._check_read_mode()
        data = self.file.read(4)
        return get_int32(data, self.endianess)

    def read_uint32(self) -> int:
        self._check_file()
        self._check_read_mode()
        data = self.file.read(4)
        return get_uint32(data, self.endianess)

    def read_int64(self) -> int:
        self._check_file()
        self._check_read_mode()
        data = self.file.read(8)
        return get_int64(data, self.endianess)

    def read_uint64(self) -> int:
        self._check_file()
        self._check_read_mode()
        data = self.file.read(8)
        return get_uint64(data, self.endianess)

    ###
    ###
    ###

    def write_str(self, input_str: str, encoding: str = "utf8") -> bool:
        self._check_file()
        self._check_write_mode()

        try:
            data_to_write = input_str.encode(encoding)
            self.file.write(data_to_write)
        except Exception as error:
            logger.error(f"Couldn't write string to file: {error}")
            return False

        return True

    def write_bytes(self, data_to_write: bytes) -> bool:
        self._check_file()
        self._check_write_mode()
        self.file.write(data_to_write)
        return True

    def write_int8(self, value: int) -> bool:
        self._check_file()
        self._check_write_mode()
        self.file.write(set_int8(value, self.endianess))
        return True

    def write_uint8(self, value: int) -> bool:
        self._check_file()
        self._check_write_mode()
        self.file.write(set_uint8(value, self.endianess))
        return True

    def write_int16(self, value: int) -> bool:
        self._check_file()
        self._check_write_mode()
        self.file.write(set_int16(value, self.endianess))
        return True

    def write_uint16(self, value: int) -> bool:
        self._check_file()
        self._check_write_mode()
        self.file.write(set_uint16(value, self.endianess))
        return True

    def write_int24(self, value: int) -> bool:
        self._check_file()
        self._check_write_mode()
        self.file.write(set_int24(value, self.endianess))
        return True

    def write_uint24(self, value: int) -> bool:
        self._check_file()
        self._check_write_mode()
        self.file.write(set_uint24(value, self.endianess))
        return True

    def write_int32(self, value: int) -> bool:
        self._check_file()
        self._check_write_mode()
        self.file.write(set_int32(value, self.endianess))
        return True

    def write_uint32(self, value: int) -> bool:
        self._check_file()
        self._check_write_mode()
        self.file.write(set_uint32(value, self.endianess))
        return True

    def write_int64(self, value: int) -> bool:
        self._check_file()
        self._check_write_mode()
        self.file.write(set_int64(value, self.endianess))
        return True

    def write_uint64(self, value: int) -> bool:
        self._check_file()
        self._check_write_mode()
        self.file.write(set_uint64(value, self.endianess))
        return True
