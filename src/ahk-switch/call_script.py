from subprocess import run
from loguru import logger

from pathlib import Path
import sys


RUNNERS: dict[str, list[str]] = {
    ".py": [sys.executable],
    ".ahk": ["AutoHotkey.exe"],
}


def switch(path: str | Path) -> str:
    file = Path(path)
    runner = RUNNERS.get(file.suffix)
    if not runner:
        logger.error("Unknown extension: {}", file.suffix)
        return ""

    result = run(
        [*runner, str(file)],
        capture_output=True,
        text=True,
        check=False,
    )
    logger.debug("stdout: {}", result.stdout)
    logger.debug("stderr: {}", result.stderr)
    if result.returncode != 0:
        logger.error("Script failed: {}", result.stderr)

    logger.debug("stdout: {}", result.stdout)

    if result.returncode != 0:
        logger.error("Script failed: {}", result.stderr)
        return ""

    return result.stdout
