import lzma


class LzmaHandler:
    def compress_data(self, input_data: bytes) -> bytes:
        return lzma.compress(input_data)

    def decompress_data(self, compressed_data: bytes) -> bytes:
        return lzma.decompress(compressed_data)
