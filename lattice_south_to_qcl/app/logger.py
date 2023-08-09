import logging
from logging.handlers import TimedRotatingFileHandler
from decouple import config

LATTICE_LOG = config("Logs_path")

print(f"log file path --> {LATTICE_LOG}")

level = logging.DEBUG + 1
logging.addLevelName(level, "micro_service_four")


def log_struct(self, message, *args, **kwargs):
    if self.isEnabledFor(level):
        print("inside the if condition")
        self._log(level, message, args, **kwargs)


logging.Logger.log_struct = log_struct


def get_logger(level=logging.DEBUG):
    log_path = str(LATTICE_LOG)
    log_path = fr'{log_path}'
    logger = logging.getLogger('qcl')
    if not len(logger.handlers):
        file_handler = TimedRotatingFileHandler(log_path, when="midnight", interval=1, backupCount=60)
        file_handler.suffix = "%Y%m%d"
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(filename)20s() - %(lineno)s] [%(funcName)20s()] [%(message)s]")
        file_handler.setFormatter(formatter)
        logger.setLevel(level)
        logger.addHandler(file_handler)
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(formatter)
        logger.addHandler(consoleHandler)
    return logger
