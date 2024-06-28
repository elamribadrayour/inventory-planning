"""logger initialization."""

import logging


def init() -> None:
    """Set Logger format."""
    log_format = (
        "%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s"
    )
    logging.basicConfig(
        format=log_format,
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
