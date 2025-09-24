import bz2


class Bzip2Handler:
    def compress_data(self, input_data: bytes) -> bytes:
        return bz2.compress(input_data)

    def decompress_data(self, compressed_data: bytes) -> bytes:
        return bz2.decompress(compressed_data)
