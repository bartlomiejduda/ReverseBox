"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

# Compression used in "Data1.dat" archive file
# from game "Re:Tiyoruga"
# https://doujinstyle.com/?p=page&type=2&id=100


# fmt: off
# mypy: ignore-errors

def decompress_block(input_data: bytes, data_offset: int) -> tuple:
    compression_flag: int = input_data[data_offset]
    decompressed_block: bytearray = bytearray()
    process_block: bytes = bytearray(64)
    start_data_offset: int = data_offset
    data_offset += 1

    if compression_flag == 1:

        # initialize process block
        process_offset: int = 0
        for i in range(8):
            for x in range(8):
                processed_value: int = int(((1 << x) & input_data[data_offset+i]) != 0)
                process_block[process_offset] = processed_value
                process_offset += 1

        data_offset += 8

        # decompress block data
        for j in range(64):
            if process_block[j]:
                for k in range(16):
                    decompressed_block.extend(b'\x00')
            else:
                for m in range(16):
                    decompressed_block.append(input_data[data_offset])
                    data_offset += 1

    elif compression_flag == 0:
        decompressed_block.extend(input_data[data_offset:data_offset + 1024])
        data_offset += 1024
    else:
        raise Exception("Not supported compression flag!")

    processed_data_size: int = data_offset - start_data_offset
    return decompressed_block, processed_data_size


def decompress_data(input_data: bytes, uncompressed_data_size: int) -> bytes:
    output_decompressed_data: bytearray = bytearray()
    input_data_offset: int = 0

    while input_data_offset < len(input_data):
        decompressed_data, processed_bytes_count = decompress_block(input_data, input_data_offset)
        output_decompressed_data.extend(decompressed_data)
        input_data_offset += processed_bytes_count

    if len(output_decompressed_data) > uncompressed_data_size:
        return output_decompressed_data[:uncompressed_data_size]
    else:
        return output_decompressed_data
