import struct
from io import BufferedReader
from typing import Optional

# mypy: ignore-errors
from reversebox.common.logger import get_logger

logger = get_logger(__name__)


class FileReader:
    def __init__(self, file_path: str, open_mode: str):
        self.file_path = file_path
        self.open_mode = open_mode

        self.file: Optional[BufferedReader] = None

    def open(self) -> bool:
        self.file = open(self.file_path, self.open_mode)
        if not self.file:
            error_message = "File can't be opened!"
            logger.error(error_message)
            raise Exception(error_message)
        if "r" not in self.open_mode:
            error_message = "Wrong file open mode!"
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

    def seek(self, seek_value):
        self._check_file()
        self.file.seek(seek_value)

    def read_str(self, str_length: int, encoding: str) -> str:
        self._check_file()
        data = self.file.read(str_length)
        return data.decode(encoding)

    def read_uint32_le(self) -> int:
        self._check_file()
        data = self.file.read(4)
        return struct.unpack("<L", data)[0]

    def read_int32_le(self) -> int:
        self._check_file()
        data = self.file.read(4)
        return struct.unpack("<l", data)[0]

    def read_uint16_le(self) -> int:
        self._check_file()
        data = self.file.read(2)
        return struct.unpack("<H", data)[0]

    def read_int16_le(self) -> int:
        self._check_file()
        data = self.file.read(2)
        return struct.unpack("<h", data)[0]

    def read_uint8(self) -> int:
        self._check_file()
        data = self.file.read(1)
        return struct.unpack("B", data)[0]

    def read_int8(self) -> int:
        self._check_file()
        data = self.file.read(1)
        return struct.unpack("b", data)[0]

    def read_uint32_be(self) -> int:
        self._check_file()
        data = self.file.read(4)
        return struct.unpack(">L", data)[0]

    def read_int32_be(self) -> int:
        self._check_file()
        data = self.file.read(4)
        return struct.unpack(">l", data)[0]

    def read_uint16_be(self) -> int:
        self._check_file()
        data = self.file.read(2)
        return struct.unpack(">H", data)[0]

    def read_int16_be(self) -> int:
        self._check_file()
        data = self.file.read(2)
        return struct.unpack(">h", data)[0]
