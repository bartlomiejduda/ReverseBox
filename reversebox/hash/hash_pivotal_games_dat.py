"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import numpy as np

# Pivotal Games DAT hash
# Used for hashing filenames in DAT archives in games like:
# - Conflict: Desert Storm
# - Conflict: Desert Storm II
# - Conflict: Vietnam
# - Conflict: Global Terror
# - Conflict: Denied Ops
# - The Great Escape


class PivotalGamesDATHashHandler:
    def __init__(self):
        pass

    @staticmethod
    def calculate_pivotal_games_dat_hash_from_string(input_string: str) -> int:
        j = 0
        dw_hash = np.int32(1)
        b_counter = np.uint8(1)
        dw_blocks = 8 * len(input_string)

        if dw_blocks > 0:
            for i in range(dw_blocks):
                A = (dw_hash & 0x200000) != 0
                B = (dw_hash & 2) != 0
                C = (dw_hash & 1) != 0
                D = dw_hash < 0

                dw_hash *= 2

                X = (ord(input_string[j]) & b_counter) != 0

                if D ^ (A ^ B ^ C ^ X):
                    dw_hash |= 1

                b_counter *= 2
                if b_counter == 0:
                    j += 1
                    b_counter = np.uint8(1)

        return int(np.uint32(dw_hash))
