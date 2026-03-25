import os

from loguru import logger


SUPPORTED = {".py", ".ahk"}


def find_ahk(
    path: str = "~/.silletr-ahk-switch/",
    extension: str | set[str] = SUPPORTED,  # now accepts both
) -> list[str]:
    full_path: str = os.path.expanduser(path)
    logger.info(f"Searching from: {full_path}")

    # normalize to set so we can do `in` check either way
    exts: set[str] = {extension} if isinstance(extension, str) else set(extension)

    found_scripts: list[str] = []

    # pyright complaining on "dirs" variable
    for root, dirs, files in os.walk(top=full_path):  # pyright: ignore
        for file in files:
            if any(file.endswith(ext) for ext in exts):
                found_path: str = os.path.join(root, file)
                logger.success(f"Found: {found_path}")
                found_scripts.append(found_path)

    if not found_scripts:
        raise FileNotFoundError(f"No {extension} scripts found in {full_path}")

    return found_scripts


if __name__ == "__main__":
    find_ahk()
