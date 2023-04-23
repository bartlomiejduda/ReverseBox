"""
Copyright © 2023  Bartłomiej Duda
License: GPL-3.0 License
"""


class BytesHandler:
    def __init__(self, input_bytes: bytes):
        self.input_bytes = input_bytes

    def get_bytes(self, offset: int, size: int) -> bytes:
        # fmt: off
        output_bytes: bytes = self.input_bytes[offset: offset + size]
        # fmt: on
        return output_bytes

    def fill_to_length(self, expected_length: int, fill_byte: bytes = b"\x00") -> bytes:
        if len(fill_byte) > 1:
            raise Exception("Fill byte is too long!")

        if len(self.input_bytes) >= expected_length:
            raise Exception("Bytes sequence is longer or equal expected length!")

        length_to_fill: int = expected_length - len(self.input_bytes)
        fill_value: bytes = b""
        for _ in range(length_to_fill):
            fill_value += fill_byte
        return self.input_bytes + fill_value
