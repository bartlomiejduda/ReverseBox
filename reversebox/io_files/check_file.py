import os
from typing import Tuple


def check_file(
    in_file_path: str,
    expected_extension: str,
    file_should_exist: bool,
    create_dirs=False,
) -> Tuple[str, str]:
    if file_should_exist:
        if not os.path.isfile(in_file_path):
            return "NOT_FILE_ERROR", f"{in_file_path} is not a valid input file path!"

    in_file_extension = os.path.splitext(in_file_path)[1]
    if in_file_extension.upper() != expected_extension.upper():
        return (
            f"NOT_{expected_extension.upper()}_ERROR",
            f"{in_file_path} is not a valid {expected_extension.upper()} file!",
        )

    if create_dirs:
        if not os.path.exists(os.path.dirname(in_file_path)):
            try:
                os.makedirs(os.path.dirname(in_file_path))
            except FileNotFoundError:
                return "CANT_CREATE_DIR_ERROR", "Can't create output directory!"

    return "OK", ""
