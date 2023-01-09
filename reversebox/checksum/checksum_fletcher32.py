"""
Copyright © 2023  Bartłomiej Duda
License: GPL-3.0 License
"""

# fmt: off


class Fletcher32Handler:
    def __init__(self):
        pass

    def calculate_fletcher32(self, input_data: bytes) -> int:
        words = (input_data[i:i+2] for i in range(0, len(input_data), 2))
        sum1 = sum2 = 0
        for word in words:
            sum1 = (sum1 + int.from_bytes(word, "little")) % 0xFFFF
            sum2 = (sum2 + sum1) % 0xFFFF
        return (sum2 << 16) | sum1

# fmt: on
