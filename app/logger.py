import logging


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def prepare_logger(level):
    logger = logging.getLogger('main_logger')
    logger.setLevel(level)
    fmtr = CustomFormatter()
    ch = logging.StreamHandler()
    fh = logging.FileHandler(filename='../medCourseBot.log', mode='a', encoding='utf-8')

    ch.setLevel(level)
    fh.setLevel(level)

    ch.setFormatter(fmtr)
    fh.setFormatter(fmtr)

    logger.addHandler(ch)
    logger.addHandler(fh)

    logger.info('Logger configured...')
