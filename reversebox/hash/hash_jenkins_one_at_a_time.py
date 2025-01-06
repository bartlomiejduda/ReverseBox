"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import numpy as np

from reversebox.common.numpy_helper_functions import (
    bytes_to_byte_array,
    string_to_byte_array,
)


# https://en.wikipedia.org/wiki/Jenkins_hash_function
class JenkinsOneAtATimeHandler:
    def __init__(self):
        pass

    @staticmethod
    def calculate_jenkins_one_at_a_time_hash_from_string(input_string: str) -> int:
        byte_array = string_to_byte_array(input_string)
        h = np.uint32(0)
        for byte in byte_array:
            h += np.uint8(byte)
            h += np.uint32(h) << np.uint8(10)
            h ^= np.uint32(h) >> np.uint8(6)
        h += np.uint32(h) << np.uint8(3)
        h ^= np.uint32(h) >> np.uint8(11)
        h += np.uint32(h) << np.uint8(15)
        return int(h)

    @staticmethod
    def calculate_jenkins_one_at_a_time_hash_from_bytes(input_bytes: bytes) -> int:
        byte_array = bytes_to_byte_array(input_bytes)
        h = np.uint32(0)
        for byte in byte_array:
            h += np.uint8(byte)
            h += np.uint32(h) << np.uint8(10)
            h ^= np.uint32(h) >> np.uint8(6)
        h += np.uint32(h) << np.uint8(3)
        h ^= np.uint32(h) >> np.uint8(11)
        h += np.uint32(h) << np.uint8(15)
        return int(h)
