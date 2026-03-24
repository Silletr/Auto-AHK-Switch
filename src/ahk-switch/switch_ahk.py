import subprocess
from loguru import logger


def switch(path: str) -> None:
    logger.info(f"Switching to: {path}")
    subprocess.Popen(["python", path])
