"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import numpy as np


def string_to_byte_array(input_string: str) -> np.ndarray:
    return np.array([ord(c) for c in input_string], dtype=np.uint8)


def bytes_to_byte_array(input_bytes: bytes) -> np.ndarray:
    return np.array([b for b in input_bytes], dtype=np.uint8)
