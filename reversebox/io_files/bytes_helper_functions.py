import struct


def get_bits(number: int, number_of_bits: int, position: int) -> int:
    shifted_number = number >> (position - 1)
    mask = (1 << number_of_bits) - 1
    extracted_bits = shifted_number & mask
    extracted_number = bin(extracted_bits)[2:]
    return int(extracted_number, 2)


def get_uint8(input_bytes: bytes, endianess: str) -> int:
    result = struct.unpack(endianess + "B", input_bytes)[0]
    return result


def get_uint16(input_bytes: bytes, endianess: str) -> int:
    result = struct.unpack(endianess + "H", input_bytes)[0]
    return result


def get_uint24(input_bytes: bytes, endianess: str) -> int:
    if endianess == "<":
        result = struct.unpack(endianess + "I", input_bytes + b"\x00")[0]
    elif endianess == ">":
        result = struct.unpack(endianess + "I", b"\x00" + input_bytes)[0]
    else:
        raise Exception("Wrong endianess!")
    return result


def get_uint32(input_bytes: bytes, endianess: str) -> int:
    result = struct.unpack(endianess + "I", input_bytes)[0]
    return result
