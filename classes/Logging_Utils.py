import logging
import logging.handlers
import sys
import os

class Logging_Utils():
    
    logging_folder = "logs"
    logging_file_size_bytes = 500000
    backup_count = 2

    @staticmethod
    def setup_logging_in_main(verbose: bool = True, write_file: bool = True):
        logging_format = "| %(levelname)s | %(asctime)s | %(filename)s:%(lineno)s | %(message)s"
        stdoutHandler = logging.StreamHandler(stream=sys.stdout)
        if not os.path.isdir(__class__.logging_folder):
            os.makedirs(__class__.logging_folder)
        if (write_file): fileWritingHandler = logging.handlers.RotatingFileHandler(
            __class__.logging_folder+"/current_logs.txt",
            maxBytes=__class__.logging_file_size_bytes,
            backupCount=__class__.backup_count)
        stdoutHandler.setFormatter(logging.Formatter(logging_format))
        if (write_file): fileWritingHandler.setFormatter(stdoutHandler)
        logger = logging.getLogger("__main__")
        for hdl in logger.handlers:
            logger.removeHandler(hdl)
        logger.setLevel(logging.INFO)
        if (write_file):
            logger.addHandler(fileWritingHandler)
        if (verbose):
            logger.addHandler(stdoutHandler)
        if not (write_file or verbose):
            logger.addHandler(logging.NullHandler())


    @staticmethod
    def get_logger():
        return logging.getLogger("__main__")