import logging

root_logger = logging.getLogger("pyutil")
root_logger.setLevel(logging.INFO)
root_logger.addHandler(logging.StreamHandler())
root_logger.handlers[0].setFormatter(
    logging.Formatter(
        "{asctime}.{msecs:03.0f} {levelname:<8} {name:<50}{funcName:>35}:{lineno:<4} {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
)

from . import cache, dicts, enums, hashing, io, misc, profiling
