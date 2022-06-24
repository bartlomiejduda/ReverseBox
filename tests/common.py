from dataclasses import dataclass


@dataclass
class CRCTestEntry:
    test_data: bytes
    expected_int: int
    expected_str: str
