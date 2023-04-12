import struct
from io import BufferedReader
from typing import Optional

# mypy: ignore-errors
from reversebox.common.logger import get_logger

logger = get_logger(__name__)


class FileHandler:
    def __init__(self, file_path: str, open_mode: str, endianess_str: str = "little"):
        self.file_path = file_path
        self.open_mode = open_mode
        self.endianess = self._get_endianess(endianess_str)

        self.file: Optional[BufferedReader] = None

    def open(self) -> bool:
        self.file = open(self.file_path, self.open_mode)
        if not self.file:
            error_message = "File can't be opened!"
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

    def _check_write_mode(self) -> bool:
        if "w" not in self.open_mode:
            error_message = 'Wrong file open mode! You need to specify one of the "write" open modes!'
            logger.error(error_message)
            raise Exception(error_message)
        return True

    def seek(self, seek_value, seek_type: int = 0):
        # 0 = SEEK_SET (from file start)
        # 1 = SEEK_CUR (from current offset)
        # 2 = SEEK_END (from file end)
        self._check_file()
        self.file.seek(seek_value, seek_type)

    def get_position(self) -> int:
        self._check_file()
        return self.file.tell()

    def get_file_size(self) -> int:
        current_position = self.get_position()
        self.seek(0, 2)
        end_of_file__position = self.get_position()
        self.seek(current_position, 0)
        return end_of_file__position

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

    def read_uint32(self) -> int:
        self._check_file()
        self._check_read_mode()
        data = self.file.read(4)
        return struct.unpack(self.endianess + "L", data)[0]

    def read_int32(self) -> int:
        self._check_file()
        self._check_read_mode()
        data = self.file.read(4)
        return struct.unpack(self.endianess + "l", data)[0]

    def read_uint16(self) -> int:
        self._check_file()
        self._check_read_mode()
        data = self.file.read(2)
        return struct.unpack(self.endianess + "H", data)[0]

    def read_int16(self) -> int:
        self._check_file()
        self._check_read_mode()
        data = self.file.read(2)
        return struct.unpack(self.endianess + "h", data)[0]

    def read_uint8(self) -> int:
        self._check_file()
        self._check_read_mode()
        data = self.file.read(1)
        return struct.unpack(self.endianess + "B", data)[0]

    def read_int8(self) -> int:
        self._check_file()
        data = self.file.read(1)
        return struct.unpack(self.endianess + "b", data)[0]

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

    def write_uint32(self, value: int) -> bool:
        self._check_file()
        self._check_write_mode()
        data_to_write = struct.pack(self.endianess + "L", value)
        self.file.write(data_to_write)
        return True

    def write_int32(self, value: int) -> bool:
        self._check_file()
        self._check_write_mode()
        data_to_write = struct.pack(self.endianess + "l", value)
        self.file.write(data_to_write)
        return True

    def write_uint16(self, value: int) -> bool:
        self._check_file()
        self._check_write_mode()
        data_to_write = struct.pack(self.endianess + "H", value)
        self.file.write(data_to_write)
        return True

    def write_int16(self, value: int) -> bool:
        self._check_file()
        self._check_write_mode()
        data_to_write = struct.pack(self.endianess + "h", value)
        self.file.write(data_to_write)
        return True

    def write_uint8(self, value: int) -> bool:
        self._check_file()
        self._check_write_mode()
        data_to_write = struct.pack(self.endianess + "B", value)
        self.file.write(data_to_write)
        return True

    def write_int8(self, value: int) -> bool:
        self._check_file()
        self._check_write_mode()
        data_to_write = struct.pack(self.endianess + "b", value)
        self.file.write(data_to_write)
        return True
