import struct


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
