from subprocess import run
from loguru import logger


def switch(path: str) -> None:
    logger.info(f"Switching to: {path}")
    result = run(
        ["python", path],
        capture_output=True,
        text=True,
        check=False,
    )
    logger.debug("stdout: {}", result.stdout)
    logger.debug("stderr: {}", result.stderr)
    if result.returncode != 0:
        logger.error("Script failed: {}", result.stderr)
