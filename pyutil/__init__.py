import logging

root_logger = logging.getLogger("pyutil")
root_logger.setLevel(logging.INFO)
root_logger.addHandler(logging.StreamHandler())
root_logger.handlers[0].setFormatter(logging.Formatter("{levelname:<8} {name:>30}{funcName:>35}:{lineno:<4} {message}", style="{"))
