"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import numpy as np


def string_to_byte_array(s: str) -> np.ndarray:
    return np.array([ord(c) for c in s], dtype=np.uint8)


def bytes_to_byte_array(byte: bytes) -> np.ndarray:
    return np.array([c for c in byte], dtype=np.uint8)
