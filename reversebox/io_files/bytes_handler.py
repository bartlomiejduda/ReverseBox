"""
Copyright © 2023  Bartłomiej Duda
License: GPL-3.0 License
"""


class BytesHandler:
    def __init__(self, input_bytes: bytes):
        self.input_bytes = input_bytes
        self.data_size = len(input_bytes)

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

    # TODO - test if this works
    def bytes_to_bitstring(self):
        binary_string = "".join(format(byte, "08b") for byte in self.input_bytes)
        return binary_string

    # TODO - test if this works
    def get_int_from_bits(self, n: int, start_bit: int, number_of_bits: int) -> int:
        n = n >> (31 - start_bit - number_of_bits)
        mask = ~(-1 << number_of_bits)
        result = n & mask
        return result
