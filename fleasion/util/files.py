import errno
import os
import shutil
from typing import List

from fleasion.util.constants import get_temp_folder


def replace_files(file_to_copy: str, files_to_replace: List[str]) -> None:
    temp_folder_path = get_temp_folder()

    if temp_folder_path is None:
        raise FileNotFoundError("Cannot determine temp folder location")

    copy_file_path = os.path.join(temp_folder_path, file_to_copy)

    if os.path.exists(copy_file_path):
        for file_to_replace in files_to_replace:
            new_file_path = os.path.join(temp_folder_path, file_to_replace)

            if os.path.exists(new_file_path):
                os.remove(new_file_path)
            else:
                raise FileNotFoundError(f"{file_to_replace} not found")

            try:
                shutil.copy(copy_file_path, new_file_path)
                print(f"{new_file_path} has been replaced with {copy_file_path}")
            except OSError as e:
                print(e)
    else:
        raise FileNotFoundError(f"Could not locate file to copy {copy_file_path}")


def delete_files(files_to_delete: List[str]) -> None:
    temp_folder_path = get_temp_folder()

    if temp_folder_path is None:
        raise FileNotFoundError("Cannot determine temp folder location")

    for file_to_delete in files_to_delete:
        delete_file_path = os.path.join(temp_folder_path, file_to_delete)

        if os.path.exists(delete_file_path):
            os.remove(delete_file_path)
            print(f"{file_to_delete} has been deleted")
            return

        print(f"{file_to_delete} not found")
