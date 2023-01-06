class BytesHandler:
    def __init__(self, input_bytes: bytes):
        self.input_bytes = input_bytes

    def get_bytes(self, offset: int, size: int) -> bytes:
        # fmt: off
        output_bytes: bytes = self.input_bytes[offset: offset + size]
        # fmt: on
        return output_bytes
