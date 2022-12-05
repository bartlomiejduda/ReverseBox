"""
Copyright © 2022  Bartłomiej Duda
License: GPL-3.0 License
"""


class JCALG1Handler:
    def compress_data(self, input_data: bytes) -> bytes:

        # jcalg1_dll_path = str(Path(__file__).parents[1].resolve().joinpath("external_libs").joinpath("JCALG1.dll"))
        # jcalg1_dll_file = ctypes.cdll.LoadLibrary(jcalg1_dll_path)

        # TODO - JCALG1.dll is 32-bit, so it needs to be recompiled to 64-bit first or completely rewritten

        return b"123"
