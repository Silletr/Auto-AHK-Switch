from subprocess import Popen
import os
from loguru import logger

current_process: Popen | None = None  # type: ignore


def switch(to: str) -> None:
    global current_process
    cmd: list[str] = [""]
    # Check file exists
    if not os.path.exists(path=to):
        logger.critical(f"Script {to} not found")
        return

    if to.endswith(".py"):
        cmd: list[str] = ["python", to]
    elif to.endswith(".ahk"):
        cmd: list[str] = ["AutoHotKey.exe", to]
    elif to.endswith(".sh"):
        cmd: list[str] = ["./", to]

    else:
        logger.error(f"Unkown file extension: {to}")
        return

    current_process = Popen(cmd)
    logger.success(f"Switched to: {os.path.basename(to)}")
