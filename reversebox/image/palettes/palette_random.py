"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""


# generates palette data with random values
# useful for testing
def generate_random_palette(palette_size: int = 1024) -> bytes:
    import random

    random_palette = bytearray(palette_size)
    for i in range(palette_size):
        random_palette[i] = random.randint(0, 255)
    return random_palette
