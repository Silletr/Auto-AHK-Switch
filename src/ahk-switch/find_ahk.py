import os
from loguru import logger


# === Find .ahk (BY DEFAULT) in ~/.silletr-ahk-switch/ BY DEFAULT ===
def find_ahk(
    path: str = "~/.silletr-ahk-switch/", extension: str = ".ahk"
) -> list[str]:
    full_path: str = os.path.expanduser(path)
    logger.info(f"Searching from: {full_path}")

    found_scripts: list[str] = []

    for root, dirs, files in os.walk(top=full_path):
        for file in files:
            if file.endswith(extension):
                found_path: str = os.path.join(root, file)
                logger.success(f"Found: {found_path}")
                found_scripts.append(found_path)

    if not found_scripts:
        raise FileNotFoundError(f"No {extension} scripts found in {full_path}")

    return found_scripts


def main() -> None:
    script_extension: str = input("Enter the needed script extension: \n")
    scripts: list[str] = find_ahk(
        path="~/.silletr-ahk-switch", extension=script_extension
    )
    for script in scripts:
        logger.info(script)


if __name__ == "__main__":
    main()
