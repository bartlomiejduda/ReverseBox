"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import numpy as np

# implementation of "ZipUtils::checksumPvr" from cocos2d engine
# tested on "cg001_i01.png" file from jp.okakichi.chanran (Android)


class Cocos2dPVRChecksumHandler:
    def __init__(self):
        pass

    def calculate_cocos2d_pvr_checksum(
        self, input_data: bytes, data_len: int, endianess: str = "<"
    ) -> int:
        cs = np.uint32(0)
        cslen: int = 128

        data_len = min(data_len, cslen)

        for i in range(data_len):
            byte_data = input_data[i * 4 : i * 4 + 4]
            int_data = np.frombuffer(byte_data, dtype=f"{endianess}u4")[0]
            cs ^= np.uint32(int_data)

        return int(cs)
