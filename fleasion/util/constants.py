import os
import platform
from pathlib import Path

OS_NAME = platform.system()

FLEASION_BASE_DIR = Path(__file__).parent.parent
RESOURCES_DIR = os.path.join(FLEASION_BASE_DIR, "resources")


def get_temp_folder() -> str | None:
    """
    Get roblox temp folder path
    Returns None if cannot be determined
    """
    if OS_NAME == "Windows":
        windows_temp_folder = os.getenv("TEMP")

        if windows_temp_folder:
            return os.path.join(windows_temp_folder, "roblox", "http")

        return None

    if OS_NAME == "Linux":
        return os.path.expanduser("~/.var/app/org.vinegarhq.Sober/cache/sober/http")
