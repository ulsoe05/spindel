import logging
from termcolor import colored

class CustomFormatter(logging.Formatter):
    def __init__(self, color=""):
        super().__init__()
        self.color = color
        self.format_strings = {
            logging.DEBUG: colored(
                "[%(asctime)s.%(msecs)03d][%(levelname)s][%(filename)s:%(lineno)d] %(message)s",
                color=color,
            ),
            logging.INFO: colored(
                "[%(asctime)s.%(msecs)03d][%(levelname)s][%(filename)s:%(lineno)d] %(message)s",
                color=color,
            ),
            logging.WARNING: colored(
                "[%(asctime)s.%(msecs)03d][%(levelname)s][%(filename)s:%(lineno)d] %(message)s",
                color=color,
                attrs=["bold"],
            ),
            logging.ERROR: colored(
                "[%(asctime)s.%(msecs)03d][%(levelname)s][%(filename)s:%(lineno)d] %(message)s",
                color=color,
                attrs=["bold"],
            ),
            logging.CRITICAL: colored(
                "[%(asctime)s.%(msecs)03d][%(levelname)s][%(filename)s:%(lineno)d] %(message)s",
                color=color,
                attrs=["bold"],
            ),
        }

    def format(self, record):
        log_fmt = self.format_strings.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%H:%M:%S")
        return formatter.format(record)


def make_logger(name: str, loglevel=logging.DEBUG, color="white"):
    logger = logging.getLogger(name)
    logger.setLevel(loglevel)
    ch = logging.StreamHandler()
    ch.setLevel(loglevel)
    ch.setFormatter(CustomFormatter(color))
    logger.addHandler(ch)
    return logger


def example():
    log = make_logger(name="example", loglevel=logging.DEBUG, color="yellow")
    log.debug("debug")
    log.info("info")
    log.warning("warning")
    log.error("error")
    log.critical("critical")


if __name__ == "__main__":
    example()
