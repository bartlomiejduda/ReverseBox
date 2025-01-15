"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import io
import struct
import time

import matplotlib.pyplot as plt
import numpy as np
import pytest
import rawutil

from reversebox.io_files.bytes_helper_functions import get_uint32
from tests.common import GetSetBytesEntry

# fmt: off


def _assert_get_function_performance(get_func) -> None:
    get_set_test_entries_list: list = [
        GetSetBytesEntry(value_int=15, value_bytes=b"\x0F\x00\x00\x00", endianess="<"),
        GetSetBytesEntry(value_int=0, value_bytes=b"\x00\x00\x00\x00", endianess="<"),
        GetSetBytesEntry(value_int=2, value_bytes=b"\x02\x00\x00\x00", endianess="<"),
        GetSetBytesEntry(value_int=255, value_bytes=b"\xFF\x00\x00\x00", endianess="<"),
        GetSetBytesEntry(value_int=43690, value_bytes=b"\xAA\xAA\x00\x00", endianess="<"),

        GetSetBytesEntry(value_int=15, value_bytes=b"\x00\x00\x00\x0F", endianess=">"),
        GetSetBytesEntry(value_int=0, value_bytes=b"\x00\x00\x00\x00", endianess=">"),
        GetSetBytesEntry(value_int=2, value_bytes=b"\x00\x00\x00\x02", endianess=">"),
        GetSetBytesEntry(value_int=255, value_bytes=b"\x00\x00\x00\xFF", endianess=">"),
        GetSetBytesEntry(value_int=43690, value_bytes=b"\x00\x00\xAA\xAA", endianess=">"),
    ]

    for test_entry in get_set_test_entries_list:
        input_memory_file = io.BytesIO(initial_bytes=test_entry.value_bytes)
        input_data: bytes = input_memory_file.read(len(test_entry.value_bytes))
        input_value: int = get_func(input_data, test_entry.endianess)
        assert input_value == test_entry.value_int


def _get_time_for_helper_functions(get_func) -> float:
    test_loop_range: int = 5_000

    start_time = time.time()
    for i in range(test_loop_range):
        _assert_get_function_performance(get_func)
    execution_time = time.time() - start_time
    return round(execution_time, 2)


@pytest.mark.unittest
def test_bytes_helper_functions_get_and_set_uint32_performance():

    # old logic - basic struct version
    def _function_a_get_uint32(input_bytes: bytes, endianess: str) -> int:
        return struct.unpack(endianess + "I", input_bytes)[0]

    # old logic - alternative rawutil version
    def _function_b_get_uint32(input_bytes: bytes, endianess: str) -> int:
        return rawutil.unpack(endianess + "I", input_bytes)[0]

    # experimental logic - int from bytes
    def _function_c_get_uint32(input_bytes: bytes, endianess: str) -> int:
        if endianess == "<":
            return int.from_bytes(input_bytes, signed=False, byteorder="little")
        elif endianess == ">":
            return int.from_bytes(input_bytes, signed=False, byteorder="big")
        else:
            raise Exception("Endianess not supported!")

    # experimental logic - numpy
    def _function_d_get_uint32(input_bytes: bytes, endianess: str) -> int:
        return int(np.frombuffer(input_bytes, dtype=f"{endianess}u4")[0])

    # experimental logic - bytes operations
    def _function_e_get_uint32(input_bytes: bytes, endianess: str) -> int:
        if endianess == "<":
            value = 0
            for i, byte in enumerate(input_bytes):
                value += byte << (i * 8)
            return value
        elif endianess == ">":
            value = 0
            for i, byte in enumerate(reversed(input_bytes)):
                value += byte << (i * 8)
            return value
        else:
            raise Exception("Not supported endianess!")

    # experimental logic - alternative bytes operations
    def _function_f_get_uint32(input_bytes: bytes, endianess: str) -> int:
        if endianess == "<":
            return input_bytes[0] | (input_bytes[1] << 8) | (input_bytes[2] << 16) | (input_bytes[3] << 24)
        elif endianess == ">":
            return input_bytes[3] | (input_bytes[2] << 8) | (input_bytes[1] << 16) | (input_bytes[0] << 24)
        else:
            raise Exception("Not supported endianess!")

    # experimental logic - memory view
    def _function_g_get_uint32(input_bytes: bytes, endianess: str) -> int:
        if endianess == "<":
            return int.from_bytes(memoryview(input_bytes), byteorder='little')
        elif endianess == ">":
            return int.from_bytes(memoryview(input_bytes), byteorder='big')
        else:
            raise Exception("Not supported endianess!")

    function_a_time = _get_time_for_helper_functions(_function_a_get_uint32)
    function_b_time = _get_time_for_helper_functions(_function_b_get_uint32)
    function_c_time = _get_time_for_helper_functions(_function_c_get_uint32)
    function_d_time = _get_time_for_helper_functions(_function_d_get_uint32)
    function_e_time = _get_time_for_helper_functions(_function_e_get_uint32)
    function_f_time = _get_time_for_helper_functions(_function_f_get_uint32)
    function_g_time = _get_time_for_helper_functions(_function_g_get_uint32)
    current_function_time = _get_time_for_helper_functions(get_uint32)

    debug_flag = False
    if debug_flag:
        left = [1, 2, 3, 4, 5, 6, 7]
        time_results = [function_a_time, function_b_time, function_c_time, function_d_time, function_e_time, function_f_time, function_g_time]
        tick_label = ['struct', 'rawutil', 'int', 'numpy', 'bytes1', 'bytes2', 'memory']
        plt.bar(left, time_results, tick_label=tick_label, width=0.8, color=['green'])

        plt.xlabel('')
        plt.ylabel('time in seconds')
        plt.title('ReverseBox get_uint32 performance tests')
        plt.show()

    assert current_function_time - 0.02 <= function_a_time
    assert current_function_time - 0.02 <= function_b_time
    assert current_function_time - 0.02 <= function_c_time
    assert current_function_time - 0.02 <= function_d_time
    assert current_function_time - 0.02 <= function_e_time
    assert current_function_time - 0.02 <= function_f_time
    assert current_function_time - 0.02 <= function_g_time
