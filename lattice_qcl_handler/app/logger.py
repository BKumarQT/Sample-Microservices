import logging
from logging.handlers import TimedRotatingFileHandler

MS3_LOG = "logs\qcl_transaction_handler.log"

def get_logger(level = logging.DEBUG):
	log_path = str(MS3_LOG)
	logger = logging.getLogger('qcl_transaction_handler')
	if not len(logger.handlers):
		file_handler = TimedRotatingFileHandler(log_path, when="midnight", interval=1, backupCount=60)
		file_handler.suffix = "%Y%m%d"
		formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(filename)20s() - %(lineno)s] [%(funcName)20s()] [%(message)s]")
		file_handler.setFormatter(formatter)
		logger.setLevel(level)
		logger.addHandler(file_handler)
		consoleHandler = logging.StreamHandler()
		consoleHandler.setFormatter(formatter)  
		logger.addHandler(consoleHandler)
	return logger
