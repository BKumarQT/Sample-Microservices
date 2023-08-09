import logging
from logging.handlers import TimedRotatingFileHandler

LATTICE_LOG = "logs\lattice.log"

level = logging.DEBUG + 1
logging.addLevelName(level, "POC_LOG")


def poc_log(self, message, *args, **kwargs):
    if self.isEnabledFor(level):
        self._log(level, message, args, **kwargs)


logging.Logger.poc_log = poc_log


def get_logger(level=logging.DEBUG):
    log_path = str(LATTICE_LOG)
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
