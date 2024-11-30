"""
Copyright © 2024  Bartłomiej Duda
License: GPL-3.0 License
"""

# Ver    Date        Author             Comment
# v0.1   13.06.2020  Bartlomiej Duda    Initial version
# v0.2   26.11.2020  Bartlomiej Duda    Added "expected result" and "test xor"
# v0.3   25.09.2021  Bartlomiej Duda    Added multibyte xor option
# v0.4   17.03.2024  Bartlomiej Duda    Rewritten for ReverseBox


import struct
from typing import Optional

from reversebox.encryption.encryption_xor_basic import xor_cipher_basic


def xor_basic_guess_key(
    encrypted_xor_data: bytes, decrypted_xor_data: bytes, max_xor_key_length_length: int
) -> Optional[bytes]:
    """
    Function for guessing XOR keys
    """
    xor_key = b"\x00"

    xor_range = 255**max_xor_key_length_length

    for i in range(xor_range):
        # xoring data
        xor_res = xor_cipher_basic(encrypted_xor_data, xor_key)
        if xor_res == decrypted_xor_data:
            return xor_key  # XOR key has been found!

        # increment key
        i_xor_key: int = int.from_bytes(xor_key, "little")
        i_xor_key += 1
        if i_xor_key <= 255:
            xor_key = struct.pack("B", i_xor_key)
        elif i_xor_key > 255 and i_xor_key <= 255**2:
            xor_key = struct.pack("<H", i_xor_key)
        elif i_xor_key > 255**2 and i_xor_key <= 255**4:
            xor_key = struct.pack("<L", i_xor_key)
        else:
            raise Exception("Not supported by guess key function!")

    return None  # XOR key hasn't been found
