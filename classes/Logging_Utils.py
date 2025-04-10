import logging
import logging.handlers
import sys
import os

class Logging_Utils():
    
    logging_folder = "logs"
    logging_file_size_bytes = 500000
    backup_count = 2

    @staticmethod
    def setup_logging_in_main(verbose: bool = True):
        logging_format = "| %(levelname)s | %(asctime)s | %(filename)s:%(lineno)s | %(message)s"
        stdoutHandler = logging.StreamHandler(stream=sys.stdout)
        if not os.path.isdir(__class__.logging_folder):
            os.makedirs(__class__.logging_folder)
        fileWritingHandler = logging.handlers.RotatingFileHandler(
            __class__.logging_folder+"/current_logs.txt",
            maxBytes=__class__.logging_file_size_bytes,
            backupCount=__class__.backup_count)
        stdoutHandler.setFormatter(logging.Formatter(logging_format))
        fileWritingHandler.setFormatter(stdoutHandler)
        logger = logging.getLogger("__main__")
        logger.addHandler(fileWritingHandler)
        if (verbose):
            logger.addHandler(stdoutHandler)


    @staticmethod
    def get_logger():
        return logging.getLogger("__main__")