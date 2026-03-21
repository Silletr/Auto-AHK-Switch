import os

from subprocess import (
    CalledProcessError,
    CompletedProcess,
    run,
)
from loguru import logger


# === Find AHK scripts on the most cummon places ===
def find_ahk(name: str, path: str) -> str:
    full_path = os.path.expanduser(path)  # Expand ~ to /home/UserName
    logger.info(f"Searching from: {full_path}")

    for root, dirs, files in os.walk(top=full_path):
        if name in files:
            found_path: str = os.path.join(root, name)
            logger.success(f"File found: {found_path}!")
            try:
                file_inside: CompletedProcess[str] = run(
                    args=["cat", found_path], capture_output=True, text=True, check=True
                )

                if not file_inside.stdout.strip():  # Properly check empty/whitespace
                    logger.warning(f"File on {found_path} is empty!")
                    return "File is empty"

                return f"File Path: {found_path} | Script inside:\n{file_inside.stdout}"

            except CalledProcessError as error:
                logger.error(f"STDERR: {error.stderr}")
                return f"Error reading {found_path}"

    raise FileNotFoundError(f"Script '{name}' not found starting from {full_path}!")


def main() -> None:
    result: str = find_ahk(name="test.ahk", path="~/")
    logger.info(result)


main()
