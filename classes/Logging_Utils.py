import logging
import logging.handlers
import sys
import os

class Logging_Utils():
    logging_folder = "logs"
    logging_file_size_bytes = 500000
    backup_count = 2
    logging_format = "| %(levelname)s | %(asctime)s | %(filename)s:%(lineno)s | %(message)s"

    @staticmethod
    def setup_logging_in_main(verbose: bool = True, write_file: bool = True, log_info: bool = False):
        logger = __class__.get_logger()
        __class__._reset_logging(logger)
        if verbose: __class__._setup_terminal_logging(logger)
        if write_file: __class__._setup_file_logging(logger)
        __class__._setup_logging_level(logger, log_info)
        
        if not (write_file or verbose):
            logger.addHandler(logging.NullHandler())


    @staticmethod
    def _setup_terminal_logging(logger):
        stdout = logging.StreamHandler(stream=sys.stdout)
        formater = logging.Formatter(__class__.logging_format)
        stdout.setFormatter(formater)
        logger.addHandler(stdout)


    @staticmethod
    def _setup_file_logging(logger):
        __class__._setup_file_logging_directory()
        fileWriting = logging.handlers.RotatingFileHandler(
            __class__.logging_folder+"/current_logs.txt",
            maxBytes=__class__.logging_file_size_bytes,
            backupCount=__class__.backup_count
        )
        formater = logging.Formatter(__class__.logging_format)
        fileWriting.setFormatter(formater)
        logger.addHandler(fileWriting)


    @staticmethod
    def _setup_file_logging_directory():
        if not os.path.isdir(__class__.logging_folder):
            os.makedirs(__class__.logging_folder)


    @staticmethod
    def _reset_logging(logger):
        for hdl in logger.handlers:
            logger.removeHandler(hdl)


    @staticmethod
    def _setup_logging_level(logger, log_info: bool):
        if log_info: logger.setLevel(logging.INFO)


    @staticmethod
    def get_logger():
        return logging.getLogger("__main__")